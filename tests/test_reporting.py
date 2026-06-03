from __future__ import annotations

from ai_agent_handoff_hub.models import HandoffReport, RepositorySignal, TaskItem
from ai_agent_handoff_hub.reporting import (
    build_agent_commands,
    build_google_tasks_payload,
    build_notion_payload,
)


def sample_task() -> TaskItem:
    return TaskItem(
        task_id="AIH-test",
        repo="owner/repo",
        title="CIを修正する",
        category="ci_cd",
        priority="P0",
        assigned_agent="Codex",
        status="todo",
        why="CI失敗",
        next_action="ログを確認して修正する",
        source_url="https://github.com/owner/repo/actions",
    )


def test_report_markdown_contains_task() -> None:
    task = sample_task()
    report = HandoffReport.build(
        target_repos=["owner/repo"],
        signals=[RepositorySignal(repo="owner/repo", scanned_at="now")],
        tasks=[task],
    )

    markdown = report.to_markdown()

    assert "AIH-test" in markdown
    assert "Codex" in markdown
    assert "human_blocker_count" in markdown


def test_payload_builders_include_task_id() -> None:
    task = sample_task()

    notion = build_notion_payload([task])
    google = build_google_tasks_payload([task])

    assert notion[0]["task_id"] == "AIH-test"
    assert "AIH-test" in google[0]["notes"]


def test_agent_commands_skip_human_blockers() -> None:
    human = TaskItem(
        task_id="AIH-human",
        repo="owner/repo",
        title="本人確認",
        category="human_blocker",
        priority="P0",
        assigned_agent="Human",
        status="todo",
        why="二段階認証が必要",
        next_action="人間が認証する",
        blocked_by_human=True,
        human_reason="本人確認",
    )

    commands = build_agent_commands([sample_task(), human])

    assert "AIH-test" in commands
    assert "AIH-human" not in commands
