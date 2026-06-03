from __future__ import annotations

import json
from pathlib import Path

from .models import HandoffReport, TaskItem


def write_report(report: HandoffReport, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "handoff-report.json", report.to_dict())
    (output_dir / "handoff-report.md").write_text(report.to_markdown(), encoding="utf-8")
    write_json(output_dir / "notion-payload.json", build_notion_payload(report.tasks))
    write_json(output_dir / "google-tasks-payload.json", build_google_tasks_payload(report.tasks))
    (output_dir / "agent-commands.md").write_text(build_agent_commands(report.tasks), encoding="utf-8")


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_notion_payload(tasks: list[TaskItem]) -> list[dict[str, object]]:
    return [
        {
            "task_id": task.task_id,
            "name": task.title,
            "repo": task.repo,
            "agent": task.assigned_agent,
            "priority": task.priority,
            "status": task.status,
            "human_blocker": task.blocked_by_human,
            "human_reason": task.human_reason,
            "source_url": task.source_url,
        }
        for task in tasks
    ]


def build_google_tasks_payload(tasks: list[TaskItem]) -> list[dict[str, str]]:
    return [
        {
            "title": f"[{task.priority}] {task.repo}: {task.title}",
            "notes": (
                f"task_id: {task.task_id}\n"
                f"agent: {task.assigned_agent}\n"
                f"why: {task.why}\n"
                f"next_action: {task.next_action}\n"
                f"source: {task.source_url or 'n/a'}\n"
                f"human_blocker: {task.blocked_by_human}\n"
                f"human_reason: {task.human_reason or 'AIで継続可能'}"
            ),
        }
        for task in tasks
    ]


def build_agent_commands(tasks: list[TaskItem]) -> str:
    lines = [
        "# Agent Commands",
        "",
        "このファイルはCodex / Claude Code / Geminiへ渡すための引き継ぎ指示です。",
        "Secretsの実値は書かず、必要なSecret名だけを使ってください。",
        "",
    ]
    for task in tasks:
        if task.blocked_by_human:
            continue
        lines.extend(
            [
                f"## {task.assigned_agent}: {task.task_id}",
                "",
                f"対象repo: `{task.repo}`",
                f"目的: {task.title}",
                f"理由: {task.why}",
                f"次の作業: {task.next_action}",
                "完了条件:",
                "- 変更内容をテストで検証する",
                "- README/docs/引き継ぎメモを更新する",
                "- CIが失敗した場合はログを残し、修正して再実行する",
                "- 人間が必要な場合は理由と必要操作だけを明記する",
                "",
            ]
        )
    return "\n".join(lines)
