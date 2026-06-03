from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal

AgentName = Literal["Codex", "Claude Code", "Gemini", "Human"]
TaskCategory = Literal[
    "implementation",
    "documentation",
    "initial_setup",
    "ci_cd",
    "research",
    "review",
    "human_blocker",
]
Priority = Literal["P0", "P1", "P2", "P3"]


@dataclass(frozen=True)
class StalledItem:
    number: int
    title: str
    url: str
    updated_at: str
    kind: Literal["issue", "pull_request"]


@dataclass(frozen=True)
class RepositorySignal:
    repo: str
    scanned_at: str
    missing_readme: bool = False
    missing_docs: bool = False
    stale_issues: list[StalledItem] = field(default_factory=list)
    stale_pull_requests: list[StalledItem] = field(default_factory=list)
    failing_workflows: list[str] = field(default_factory=list)
    setup_keywords: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    source_url: str | None = None


@dataclass(frozen=True)
class TaskItem:
    task_id: str
    repo: str
    title: str
    category: TaskCategory
    priority: Priority
    assigned_agent: AgentName
    status: str
    why: str
    next_action: str
    source_url: str | None = None
    blocked_by_human: bool = False
    human_reason: str | None = None

    def to_markdown(self) -> str:
        return (
            f"### {self.task_id}: {self.title}\n\n"
            f"- repo: `{self.repo}`\n"
            f"- category: `{self.category}`\n"
            f"- priority: `{self.priority}`\n"
            f"- assigned_agent: `{self.assigned_agent}`\n"
            f"- status: `{self.status}`\n"
            f"- human_blocker: {self.blocked_by_human}\n"
            f"- human_reason: {self.human_reason or 'AIで継続可能'}\n"
            f"- why: {self.why}\n"
            f"- next_action: {self.next_action}\n"
            f"- source: {self.source_url or 'n/a'}\n"
        )


@dataclass(frozen=True)
class HandoffReport:
    generated_at: str
    target_repos: list[str]
    signals: list[RepositorySignal]
    tasks: list[TaskItem]
    summary: dict[str, Any]

    @classmethod
    def build(
        cls,
        *,
        target_repos: list[str],
        signals: list[RepositorySignal],
        tasks: list[TaskItem],
    ) -> "HandoffReport":
        by_agent: dict[str, int] = {}
        by_priority: dict[str, int] = {}
        for task in tasks:
            by_agent[task.assigned_agent] = by_agent.get(task.assigned_agent, 0) + 1
            by_priority[task.priority] = by_priority.get(task.priority, 0) + 1
        return cls(
            generated_at=datetime.now(timezone.utc).isoformat(),
            target_repos=target_repos,
            signals=signals,
            tasks=tasks,
            summary={
                "task_count": len(tasks),
                "human_blocker_count": sum(1 for task in tasks if task.blocked_by_human),
                "by_agent": by_agent,
                "by_priority": by_priority,
                "repos_scanned": len(signals),
            },
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_markdown(self) -> str:
        lines = [
            "# AI Agent Handoff Report",
            "",
            f"generated_at: `{self.generated_at}`",
            "",
            "## Summary",
        ]
        for key, value in self.summary.items():
            lines.append(f"- {key}: {value}")
        lines.extend(["", "## Tasks", ""])
        lines.extend(task.to_markdown() for task in self.tasks)
        return "\n".join(lines)
