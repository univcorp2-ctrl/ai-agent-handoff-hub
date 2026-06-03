from __future__ import annotations

from ai_agent_handoff_hub.models import RepositorySignal, StalledItem
from ai_agent_handoff_hub.planner import build_tasks


def test_build_tasks_assigns_docs_to_claude_code() -> None:
    signal = RepositorySignal(repo="owner/repo", scanned_at="2026-01-01T00:00:00+00:00", missing_readme=True, missing_docs=True)

    tasks = build_tasks([signal])

    assert len(tasks) == 2
    assert {task.assigned_agent for task in tasks} == {"Claude Code"}
    assert all(task.priority == "P1" for task in tasks)


def test_build_tasks_assigns_ci_failure_to_codex() -> None:
    signal = RepositorySignal(
        repo="owner/repo",
        scanned_at="2026-01-01T00:00:00+00:00",
        failing_workflows=["https://github.com/owner/repo/actions/runs/1"],
    )

    tasks = build_tasks([signal])

    assert len(tasks) == 1
    assert tasks[0].assigned_agent == "Codex"
    assert tasks[0].priority == "P0"
    assert tasks[0].category == "ci_cd"


def test_build_tasks_assigns_research_issue_to_gemini() -> None:
    signal = RepositorySignal(
        repo="owner/repo",
        scanned_at="2026-01-01T00:00:00+00:00",
        stale_issues=[
            StalledItem(
                number=7,
                title="外部APIの調査と検証",
                url="https://github.com/owner/repo/issues/7",
                updated_at="2025-01-01T00:00:00Z",
                kind="issue",
            )
        ],
    )

    tasks = build_tasks([signal])

    assert len(tasks) == 1
    assert tasks[0].assigned_agent == "Gemini"
    assert tasks[0].category == "research"


def test_warning_becomes_human_blocker() -> None:
    signal = RepositorySignal(
        repo="owner/repo",
        scanned_at="2026-01-01T00:00:00+00:00",
        warnings=["repo_metadata_unavailable"],
    )

    tasks = build_tasks([signal])

    assert len(tasks) == 1
    assert tasks[0].assigned_agent == "Human"
    assert tasks[0].blocked_by_human is True
