from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen

from ..models import TaskItem
from ..reporting import build_google_tasks_payload


@dataclass(frozen=True)
class GoogleTasksSyncResult:
    enabled: bool
    pushed: int
    skipped_reason: str | None = None


class GoogleTasksClient:
    def __init__(self, token: str | None, tasklist_id: str | None, webhook_url: str | None) -> None:
        self.token = token
        self.tasklist_id = tasklist_id
        self.webhook_url = webhook_url

    def sync_tasks(self, tasks: list[TaskItem]) -> GoogleTasksSyncResult:
        payloads = build_google_tasks_payload(tasks)
        if self.webhook_url:
            post_json(self.webhook_url, {"tasks": payloads}, {})
            return GoogleTasksSyncResult(True, len(payloads))
        if not self.token or not self.tasklist_id:
            return GoogleTasksSyncResult(
                False,
                0,
                "Google Tasks token/list id or webhook URL is not configured",
            )
        for payload in payloads:
            self._insert_task(payload)
        return GoogleTasksSyncResult(True, len(payloads))

    def _insert_task(self, payload: dict[str, str]) -> Any:
        url = f"https://tasks.googleapis.com/tasks/v1/lists/{quote(self.tasklist_id or '')}/tasks"
        return post_json(url, payload, {"Authorization": f"Bearer {self.token}"})


def post_json(url: str, payload: dict[str, Any], headers: dict[str, str]) -> Any:
    body = json.dumps(payload).encode("utf-8")
    request = Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    with urlopen(request, timeout=20) as response:  # noqa: S310
        raw = response.read().decode("utf-8")
        return json.loads(raw) if raw else {"ok": True}
