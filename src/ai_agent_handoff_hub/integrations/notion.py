from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.request import Request, urlopen

from ..models import TaskItem


@dataclass(frozen=True)
class NotionSyncResult:
    enabled: bool
    pushed: int
    skipped_reason: str | None = None


class NotionClient:
    def __init__(self, token: str | None, database_id: str | None) -> None:
        self.token = token
        self.database_id = database_id

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
        return post_json(
            "https://api.notion.com/v1/pages",
            payload,
            {
                "Authorization": f"Bearer {self.token}",
                "Notion-Version": "2022-06-28",
            },
        )


def post_json(url: str, payload: dict[str, Any], headers: dict[str, str]) -> Any:
    body = json.dumps(payload).encode("utf-8")
    request = Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    with urlopen(request, timeout=20) as response:  # noqa: S310
        return json.loads(response.read().decode("utf-8"))
