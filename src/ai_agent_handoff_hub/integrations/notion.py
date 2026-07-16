from __future__ import annotations

import hashlib
import json
import math
import mimetypes
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from ..models import TaskItem

NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_TASKS_VERSION = "2022-06-28"
NOTION_FILE_UPLOAD_VERSION = "2026-03-11"
MAX_SINGLE_PART_BYTES = 20 * 1024 * 1024
MULTI_PART_CHUNK_BYTES = 10 * 1024 * 1024
RETRYABLE_STATUS_CODES = {429, 500, 503, 504, 529}
SUPPORTED_IMAGE_MIME_TYPES = {
    "image/gif",
    "image/heic",
    "image/jpeg",
    "image/png",
    "image/svg+xml",
    "image/tiff",
    "image/webp",
    "image/vnd.microsoft.icon",
    "image/bmp",
    "image/avif",
    "image/apng",
}


@dataclass(frozen=True)
class NotionSyncResult:
    enabled: bool
    pushed: int
    skipped_reason: str | None = None


@dataclass(frozen=True)
class NotionImageUploadResult:
    attached: bool
    file_upload_id: str | None
    block_id: str | None
    verified: bool
    sha256: str | None
    size_bytes: int | None
    content_type: str | None
    error: str | None = None


class NotionApiError(RuntimeError):
    def __init__(self, message: str, *, status_code: int | None = None, body: str = "") -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class NotionClient:
    def __init__(
        self,
        token: str | None,
        database_id: str | None = None,
        *,
        timeout: int = 30,
        max_retries: int = 3,
        sleeper: Callable[[float], None] = time.sleep,
    ) -> None:
        self.token = token
        self.database_id = database_id
        self.timeout = timeout
        self.max_retries = max_retries
        self.sleeper = sleeper

    def sync_tasks(self, tasks: list[TaskItem]) -> NotionSyncResult:
        if not self.token or not self.database_id:
            return NotionSyncResult(
                False,
                0,
                "NOTION_TOKEN or NOTION_DATABASE_ID is not configured",
            )
        pushed = 0
        for task in tasks:
            self._create_page(task)
            pushed += 1
        return NotionSyncResult(True, pushed)

    def upload_image(
        self,
        page_or_block_id: str,
        file_path: str | Path,
        *,
        caption: str | None = None,
        verify: bool = True,
    ) -> NotionImageUploadResult:
        """Upload an image to Notion-managed storage and attach it as an image block.

        This uses Notion's official File Upload API instead of relying on Google Drive viewer
        links or other authenticated URLs. The uploaded file must be attached within one hour;
        this method performs upload and attachment in one operation and verifies the new block.
        """
        if not self.token:
            return NotionImageUploadResult(
                False,
                None,
                None,
                False,
                None,
                None,
                None,
                "NOTION_TOKEN is not configured",
            )

        try:
            path = Path(file_path).expanduser().resolve(strict=True)
            if not path.is_file():
                raise ValueError(f"Not a file: {path}")

            content_type = _detect_image_content_type(path)
            size_bytes = path.stat().st_size
            if size_bytes <= 0:
                raise ValueError("Image file is empty")
            workspace_limit = self._get_workspace_file_limit()
            if workspace_limit is not None and size_bytes > workspace_limit:
                raise ValueError(
                    f"File is {size_bytes} bytes, exceeding the Notion workspace limit "
                    f"of {workspace_limit} bytes"
                )

            sha256 = _sha256_file(path)
            number_of_parts = max(1, math.ceil(size_bytes / MULTI_PART_CHUNK_BYTES))
            mode = "single_part" if size_bytes <= MAX_SINGLE_PART_BYTES else "multi_part"
            if mode == "multi_part" and number_of_parts > 1000:
                raise ValueError("File requires more than 1000 upload parts")

            upload = self._create_file_upload(
                filename=path.name,
                content_type=content_type,
                mode=mode,
                number_of_parts=number_of_parts,
            )
            file_upload_id = str(upload["id"])
            self._send_file_upload(
                file_upload_id,
                path,
                content_type,
                mode=mode,
                number_of_parts=number_of_parts,
            )
            if mode == "multi_part":
                self._complete_file_upload(file_upload_id)

            block = self._append_image_block(
                page_or_block_id,
                file_upload_id,
                caption=caption,
            )
            block_id = str(block["id"])
            verified = self._verify_image_block(block_id) if verify else False
            if verify and not verified:
                raise NotionApiError(f"Image block verification failed for block {block_id}")

            return NotionImageUploadResult(
                True,
                file_upload_id,
                block_id,
                verified,
                sha256,
                size_bytes,
                content_type,
            )
        except (OSError, ValueError, KeyError, NotionApiError) as exc:
            return NotionImageUploadResult(
                False,
                locals().get("file_upload_id"),
                locals().get("block_id"),
                False,
                locals().get("sha256"),
                locals().get("size_bytes"),
                locals().get("content_type"),
                str(exc),
            )

    def _create_page(self, task: TaskItem) -> Any:
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Name": {"title": [{"text": {"content": task.title[:1900]}}]},
                "Task ID": {"rich_text": [{"text": {"content": task.task_id}}]},
                "Repo": {"rich_text": [{"text": {"content": task.repo}}]},
                "Agent": {"select": {"name": task.assigned_agent}},
                "Priority": {"select": {"name": task.priority}},
                "Status": {"select": {"name": task.status}},
            },
        }
        return self._request_json(
            "POST",
            "/pages",
            payload,
            notion_version=NOTION_TASKS_VERSION,
        )

    def _get_workspace_file_limit(self) -> int | None:
        response = self._request_json(
            "GET",
            "/users/me",
            notion_version=NOTION_FILE_UPLOAD_VERSION,
        )
        limit = (
            response.get("bot", {})
            .get("workspace_limits", {})
            .get("max_file_upload_size_in_bytes")
        )
        return int(limit) if isinstance(limit, int) else None

    def _create_file_upload(
        self,
        *,
        filename: str,
        content_type: str,
        mode: str,
        number_of_parts: int,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "mode": mode,
            "filename": filename,
            "content_type": content_type,
        }
        if mode == "multi_part":
            payload["number_of_parts"] = number_of_parts
        response = self._request_json(
            "POST",
            "/file_uploads",
            payload,
            notion_version=NOTION_FILE_UPLOAD_VERSION,
        )
        if response.get("status") not in {"pending", "uploaded"}:
            raise NotionApiError(f"Unexpected file upload status: {response.get('status')}")
        return response

    def _send_file_upload(
        self,
        file_upload_id: str,
        path: Path,
        content_type: str,
        *,
        mode: str,
        number_of_parts: int,
    ) -> None:
        with path.open("rb") as file_handle:
            for part_number in range(1, number_of_parts + 1):
                chunk = file_handle.read(
                    MAX_SINGLE_PART_BYTES if mode == "single_part" else MULTI_PART_CHUNK_BYTES
                )
                if not chunk and path.stat().st_size > 0:
                    raise NotionApiError(
                        f"Unexpected end of file while reading upload part {part_number}"
                    )
                body, content_header = build_multipart_body(
                    chunk,
                    filename=path.name,
                    content_type=content_type,
                    part_number=part_number if mode == "multi_part" else None,
                )
                response = self._request_json_bytes(
                    "POST",
                    f"/file_uploads/{file_upload_id}/send",
                    body,
                    content_type=content_header,
                    notion_version=NOTION_FILE_UPLOAD_VERSION,
                )
                if response.get("status") not in {"pending", "uploaded"}:
                    raise NotionApiError(
                        f"Unexpected file upload status after part {part_number}: "
                        f"{response.get('status')}"
                    )

    def _complete_file_upload(self, file_upload_id: str) -> None:
        response = self._request_json(
            "POST",
            f"/file_uploads/{file_upload_id}/complete",
            notion_version=NOTION_FILE_UPLOAD_VERSION,
        )
        if response.get("status") != "uploaded":
            raise NotionApiError(f"File upload did not complete: {response.get('status')}")

    def _append_image_block(
        self,
        page_or_block_id: str,
        file_upload_id: str,
        *,
        caption: str | None,
    ) -> dict[str, Any]:
        rich_caption: list[dict[str, Any]] = []
        if caption:
            rich_caption = [
                {
                    "type": "text",
                    "text": {"content": caption[:2000]},
                }
            ]
        payload = {
            "children": [
                {
                    "object": "block",
                    "type": "image",
                    "image": {
                        "type": "file_upload",
                        "file_upload": {"id": file_upload_id},
                        "caption": rich_caption,
                    },
                }
            ]
        }
        response = self._request_json(
            "PATCH",
            f"/blocks/{page_or_block_id}/children",
            payload,
            notion_version=NOTION_FILE_UPLOAD_VERSION,
        )
        results = response.get("results") or []
        if not results or results[0].get("type") != "image":
            raise NotionApiError("Notion did not return the newly appended image block")
        return results[0]

    def _verify_image_block(self, block_id: str) -> bool:
        block = self._request_json(
            "GET",
            f"/blocks/{block_id}",
            notion_version=NOTION_FILE_UPLOAD_VERSION,
        )
        return (
            block.get("object") == "block"
            and block.get("type") == "image"
            and not block.get("archived", False)
            and not block.get("in_trash", False)
        )

    def _request_json(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
        *,
        notion_version: str,
    ) -> dict[str, Any]:
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        return self._request_json_bytes(
            method,
            path,
            body,
            content_type="application/json" if body is not None else None,
            notion_version=notion_version,
        )

    def _request_json_bytes(
        self,
        method: str,
        path: str,
        body: bytes | None,
        *,
        content_type: str | None,
        notion_version: str,
    ) -> dict[str, Any]:
        if not self.token:
            raise NotionApiError("NOTION_TOKEN is not configured")
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": notion_version,
            "Accept": "application/json",
        }
        if content_type:
            headers["Content-Type"] = content_type

        url = f"{NOTION_API_BASE}{path}"
        for attempt in range(self.max_retries + 1):
            request = Request(url, data=body, headers=headers, method=method)
            try:
                with urlopen(request, timeout=self.timeout) as response:  # noqa: S310
                    raw = response.read().decode("utf-8")
                    return json.loads(raw) if raw else {}
            except HTTPError as exc:
                error_body = exc.read().decode("utf-8", errors="replace")
                if exc.code in RETRYABLE_STATUS_CODES and attempt < self.max_retries:
                    self.sleeper(_retry_delay(attempt, exc.headers.get("Retry-After")))
                    continue
                raise NotionApiError(
                    f"Notion API {method} {path} failed with HTTP {exc.code}: {error_body}",
                    status_code=exc.code,
                    body=error_body,
                ) from exc
            except URLError as exc:
                if attempt < self.max_retries:
                    self.sleeper(_retry_delay(attempt, None))
                    continue
                raise NotionApiError(
                    f"Notion API {method} {path} network error: {exc.reason}"
                ) from exc
        raise NotionApiError(f"Notion API {method} {path} exhausted retries")


def _detect_image_content_type(path: Path) -> str:
    content_type, _ = mimetypes.guess_type(path.name)
    if content_type not in SUPPORTED_IMAGE_MIME_TYPES:
        raise ValueError(
            f"Unsupported Notion image type for {path.name}: {content_type or 'unknown'}"
        )
    return content_type


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_multipart_body(
    file_bytes: bytes,
    *,
    filename: str,
    content_type: str,
    part_number: int | None = None,
) -> tuple[bytes, str]:
    boundary = f"----ai-agent-handoff-{uuid.uuid4().hex}"
    fallback_filename = "upload" + Path(filename).suffix.lower()
    encoded_filename = quote(filename, safe="")
    sections = [
        f"--{boundary}\r\n".encode("ascii"),
        (
            'Content-Disposition: form-data; name="file"; '
            f'filename="{fallback_filename}"; filename*=UTF-8\'\'{encoded_filename}\r\n'
        ).encode("ascii"),
        f"Content-Type: {content_type}\r\n\r\n".encode("ascii"),
        file_bytes,
        b"\r\n",
    ]
    if part_number is not None:
        sections.extend(
            [
                f"--{boundary}\r\n".encode("ascii"),
                b'Content-Disposition: form-data; name="part_number"\r\n\r\n',
                str(part_number).encode("ascii"),
                b"\r\n",
            ]
        )
    sections.append(f"--{boundary}--\r\n".encode("ascii"))
    return b"".join(sections), f"multipart/form-data; boundary={boundary}"


def _retry_delay(attempt: int, retry_after: str | None) -> float:
    if retry_after:
        try:
            return max(0.0, float(retry_after))
        except ValueError:
            pass
    return min(2**attempt, 8)


def post_json(url: str, payload: dict[str, Any], headers: dict[str, str]) -> Any:
    """Backward-compatible helper retained for external callers."""
    body = json.dumps(payload).encode("utf-8")
    request = Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    with urlopen(request, timeout=20) as response:  # noqa: S310
        return json.loads(response.read().decode("utf-8"))
