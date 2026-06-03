from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


class GitHubApiError(RuntimeError):
    pass


@dataclass(frozen=True)
class GitHubClient:
    token: str | None
    base_url: str = "https://api.github.com"

    def _request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "ai-agent-handoff-hub",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = Request(
            f"{self.base_url}{path}",
            data=body,
            headers=headers,
            method=method,
        )
        try:
            with urlopen(request, timeout=20) as response:  # noqa: S310 - fixed GitHub API URL
                data = response.read().decode("utf-8")
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise GitHubApiError(f"GitHub API {method} {path} failed: {exc.code} {detail}") from exc
        except URLError as exc:
            raise GitHubApiError(f"GitHub API {method} {path} failed: {exc}") from exc
        if not data:
            return None
        return json.loads(data)

    def get_repo(self, full_name: str) -> dict[str, Any]:
        owner, repo = split_repo(full_name)
        return self._request("GET", f"/repos/{quote(owner)}/{quote(repo)}")

    def get_readme(self, full_name: str) -> dict[str, Any]:
        owner, repo = split_repo(full_name)
        return self._request("GET", f"/repos/{quote(owner)}/{quote(repo)}/readme")

    def get_contents(self, full_name: str, path: str) -> Any:
        owner, repo = split_repo(full_name)
        return self._request("GET", f"/repos/{quote(owner)}/{quote(repo)}/contents/{quote(path)}")

    def list_open_issues_and_prs(self, full_name: str) -> list[dict[str, Any]]:
        owner, repo = split_repo(full_name)
        return self._request(
            "GET",
            f"/repos/{quote(owner)}/{quote(repo)}/issues?state=open&per_page=100&sort=updated&direction=asc",
        )

    def list_workflow_runs(self, full_name: str) -> dict[str, Any]:
        owner, repo = split_repo(full_name)
        return self._request("GET", f"/repos/{quote(owner)}/{quote(repo)}/actions/runs?per_page=10")

    def create_issue(self, full_name: str, *, title: str, body: str, labels: list[str] | None = None) -> dict[str, Any]:
        owner, repo = split_repo(full_name)
        return self._request(
            "POST",
            f"/repos/{quote(owner)}/{quote(repo)}/issues",
            {"title": title, "body": body, "labels": labels or ["ai-handoff"]},
        )


def split_repo(full_name: str) -> tuple[str, str]:
    parts = full_name.split("/")
    if len(parts) != 2 or not all(parts):
        raise ValueError(f"Repository must be in owner/repo format: {full_name!r}")
    return parts[0], parts[1]
