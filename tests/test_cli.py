from __future__ import annotations

from ai_agent_handoff_hub.cli import issue_labels
from ai_agent_handoff_hub.models import TaskItem


def test_issue_labels() -> None:
    task = TaskItem(
        task_id="AIH-1",
        repo="owner/repo",
        title="Fix CI",
        category="ci_cd",
        priority="P0",
        assigned_agent="Codex",
        status="todo",
        why="CI failed",
        next_action="Fix tests",
    )

    assert issue_labels(task) == ["ai-handoff", "agent:Codex", "priority:P0"]
