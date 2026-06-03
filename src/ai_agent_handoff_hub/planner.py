from __future__ import annotations

import hashlib
from typing import cast

from .models import AgentName, Priority, RepositorySignal, StalledItem, TaskCategory, TaskItem


def build_tasks(signals: list[RepositorySignal]) -> list[TaskItem]:
    tasks: list[TaskItem] = []
    for signal in signals:
        tasks.extend(tasks_for_signal(signal))
    return dedupe_tasks(tasks)


def tasks_for_signal(signal: RepositorySignal) -> list[TaskItem]:
    tasks: list[TaskItem] = []
    if signal.missing_readme:
        tasks.append(
            make_task(
                signal,
                title="READMEの先頭に全体像・画像・初期設定手順を追加する",
                category="documentation",
                priority="P1",
                agent="Claude Code",
                why="READMEが見つからないため、次のAIや人間が最短で理解できない。",
                next_action="概要、実行方法、Secrets一覧、未完了タスクの引き継ぎ方を書く。",
            )
        )
    if signal.missing_docs:
        tasks.append(
            make_task(
                signal,
                title="docs/architecture.md と docs/setup.md を整備する",
                category="documentation",
                priority="P1",
                agent="Claude Code",
                why="アーキテクチャと初期設定が文書化されていない。",
                next_action="Mermaid図、Secrets名、CI/CD、外部連携、手動作業をdocsに残す。",
            )
        )
    tasks.extend(task_from_stalled_issue(signal, item) for item in signal.stale_issues)
    tasks.extend(task_from_stalled_pr(signal, item) for item in signal.stale_pull_requests)
    tasks.extend(task_from_workflow_failure(signal, url) for url in signal.failing_workflows)
    tasks.extend(task_from_setup_keyword(signal, keyword) for keyword in signal.setup_keywords)
    tasks.extend(task_from_warning(signal, warning) for warning in signal.warnings)
    return tasks


def task_from_stalled_issue(signal: RepositorySignal, item: StalledItem) -> TaskItem:
    title_lower = item.title.lower()
    if any(word in title_lower for word in ("doc", "readme", "setup", "初期設定", "手順")):
        category: TaskCategory = "documentation"
        agent: AgentName = "Claude Code"
    elif any(word in title_lower for word in ("research", "調査", "検証", "qa")):
        category = "research"
        agent = "Gemini"
    else:
        category = "implementation"
        agent = "Codex"
    return make_task(
        signal,
        title=f"停滞Issue #{item.number} を再開して完了まで進める: {item.title}",
        category=category,
        priority="P1",
        agent=agent,
        why=f"Issueが長期間更新されていない: updated_at={item.updated_at}",
        next_action="Issue本文とコメントを読み、未完了条件を抽出して実装・テスト・docs更新まで進める。",
        source_url=item.url,
    )


def task_from_stalled_pr(signal: RepositorySignal, item: StalledItem) -> TaskItem:
    return make_task(
        signal,
        title=f"放置PR #{item.number} をレビューし、マージ可能状態または修正Issueへ整理する",
        category="review",
        priority="P1",
        agent="Codex",
        why=f"PRが長期間更新されていない: {item.title}",
        next_action="差分確認、テスト実行、競合解消、レビューコメント対応、必要なら新Issue化する。",
        source_url=item.url,
    )


def task_from_workflow_failure(signal: RepositorySignal, workflow_url: str) -> TaskItem:
    return make_task(
        signal,
        title="CI失敗ログを解析して修正し、再実行する",
        category="ci_cd",
        priority="P0",
        agent="Codex",
        why="CIが失敗しているため、本番準備に進めない。",
        next_action="Actionsログを取得し、失敗箇所を修正してテストを再実行する。",
        source_url=workflow_url,
    )


def task_from_setup_keyword(signal: RepositorySignal, keyword: str) -> TaskItem:
    return make_task(
        signal,
        title=f"初期設定タスクをAI実行可能な手順へ分解する: {keyword}",
        category="initial_setup",
        priority="P1",
        agent="Claude Code",
        why="初期設定・認証・API連携に関する未完了タスクがある。",
        next_action="AIが実行できる作業、Secretsが必要な作業、人間が必要な作業に分解する。",
    )


def task_from_warning(signal: RepositorySignal, warning: str) -> TaskItem:
    return make_task(
        signal,
        title="GitHubスキャン権限またはAPI接続を確認する",
        category="human_blocker",
        priority="P0",
        agent="Human",
        why=warning,
        next_action="GH_PATの権限、対象repoの可視性、Actionsの権限を確認する。",
        blocked_by_human=True,
        human_reason="GitHub APIへアクセスするための認可や対象repo権限は人間操作が必要です。",
    )


def make_task(
    signal: RepositorySignal,
    *,
    title: str,
    category: TaskCategory,
    priority: str,
    agent: AgentName,
    why: str,
    next_action: str,
    source_url: str | None = None,
    blocked_by_human: bool = False,
    human_reason: str | None = None,
) -> TaskItem:
    return TaskItem(
        task_id=stable_task_id(signal.repo, title),
        repo=signal.repo,
        title=title,
        category=category,
        priority=cast(Priority, priority),
        assigned_agent=agent,
        status="todo",
        why=why,
        next_action=next_action,
        source_url=source_url or signal.source_url,
        blocked_by_human=blocked_by_human,
        human_reason=human_reason,
    )


def stable_task_id(repo: str, title: str) -> str:
    digest = hashlib.sha1(f"{repo}:{title}".encode("utf-8")).hexdigest()[:8]
    return f"AIH-{digest}"


def dedupe_tasks(tasks: list[TaskItem]) -> list[TaskItem]:
    seen: set[str] = set()
    result: list[TaskItem] = []
    for task in tasks:
        if task.task_id not in seen:
            seen.add(task.task_id)
            result.append(task)
    return result
