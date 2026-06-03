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
        blocker = "あり" if self.blocked_by_human else "なし"
        human_reason = self.human_reason or "AIで継続可能"
        return (
            f"### {self.task_id}: {self.title}\n\n"
            f"- repo: `{self.repo}`\n"
            f"- category: `{self.category}`\n"
            f"- priority: `{self.priority}`\n"
            f"- assigned_agent: `{self.assigned_agent}`\n"
            f"- status: `{self.status}`\n"
            f"- human_blocker: {blocker}\n"
            f"- human_reason: {human_reason}\n"
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
    def build(cls, *, target_repos: list[str], signals: list[RepositorySignal], tasks: list[TaskItem]) -> "HandoffReport":
        human_blockers = [task for task in tasks if task.blocked_by_human]
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
                "human_blocker_count": len(human_blockers),
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
            f"target_repos: `{', '.join(self.target_repos) or 'none'}`",
            "",
            "## Summary",
            "",
            f"- task_count: {self.summary['task_count']}",
            f"- human_blocker_count: {self.summary['human_blocker_count']}",
            f"- repos_scanned: {self.summary['repos_scanned']}",
            f"- by_agent: `{self.summary['by_agent']}`",
            f"- by_priority: `{self.summary['by_priority']}`",
            "",
            "## Tasks",
            "",
        ]
        if not self.tasks:
            lines.append("未完了タスクは検出されませんでした。")
        else:
            for task in self.tasks:
                lines.append(task.to_markdown())
        lines.extend(["", "## Signals", ""])
        for signal in self.signals:
            lines.append(f"### {signal.repo}")
            lines.append(f"- missing_readme: {signal.missing_readme}")
            lines.append(f"- missing_docs: {signal.missing_docs}")
            lines.append(f"- stale_issues: {len(signal.stale_issues)}")
            lines.append(f"- stale_pull_requests: {len(signal.stale_pull_requests)}")
            lines.append(f"- failing_workflows: {len(signal.failing_workflows)}")
            lines.append(f"- setup_keywords: {', '.join(signal.setup_keywords) or 'none'}")
            lines.append(f"- warnings: {', '.join(signal.warnings) or 'none'}")
            lines.append("")
        return "\n".join(lines)
