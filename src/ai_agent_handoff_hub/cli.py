from __future__ import annotations

import argparse
import sys

from .config import AppConfig
from .github_api import GitHubClient
from .integrations.google_tasks import GoogleTasksClient
from .integrations.notion import NotionClient
from .models import HandoffReport, TaskItem
from .planner import build_tasks
from .reporting import write_report
from .scanner import scan_repositories


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI Agent Handoff Hub")
    sub = parser.add_subparsers(dest="command", required=True)
    run_all = sub.add_parser(
        "run-all",
        help="Scan repos, build handoff tasks, write reports, and sync integrations",
    )
    run_all.add_argument("--target-repos", default=None, help="Comma separated owner/repo list")
    run_all.add_argument("--stale-days", type=int, default=None)
    run_all.add_argument("--output-dir", default=None)
    run_all.add_argument("--dry-run", action="store_true")
    run_all.add_argument("--create-github-issues", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "run-all":
        return run_all(args)
    raise ValueError(f"Unknown command: {args.command}")


def run_all(args: argparse.Namespace) -> int:
    config = AppConfig.from_env(
        target_repos=args.target_repos,
        stale_days=args.stale_days,
        output_dir=args.output_dir,
        dry_run=args.dry_run,
    )
    if not config.target_repos:
        print("No target repos specified. Use --target-repos owner/repo or TARGET_REPOS.", file=sys.stderr)
        return 2

    client = GitHubClient(config.github_token)
    signals = scan_repositories(client, config.target_repos, config.stale_days)
    tasks = build_tasks(signals)
    report = HandoffReport.build(
        target_repos=config.target_repos,
        signals=signals,
        tasks=tasks,
    )
    write_report(report, config.output_dir)

    create_issues = args.create_github_issues or config.create_github_issues
    if create_issues and not config.dry_run:
        create_github_issues(client, tasks)

    if not config.dry_run:
        notion_result = NotionClient(config.notion_token, config.notion_database_id).sync_tasks(tasks)
        google_result = GoogleTasksClient(
            config.google_tasks_api_token,
            config.google_tasks_tasklist_id,
            config.google_tasks_webhook_url,
        ).sync_tasks(tasks)
        print(f"notion_sync={notion_result}")
        print(f"google_tasks_sync={google_result}")
    else:
        print("dry_run=true: external sync and issue creation skipped")

    print(f"tasks={len(tasks)} output_dir={config.output_dir}")
    return 0


def create_github_issues(client: GitHubClient, tasks: list[TaskItem]) -> None:
    for task in tasks:
        if task.blocked_by_human:
            continue
        client.create_issue(
            task.repo,
            title=f"[AI Handoff] {task.title}",
            body=task.to_markdown() + "\n\nCreated by AI Agent Handoff Hub.",
            labels=issue_labels(task),
        )


def issue_labels(task: TaskItem) -> list[str]:
    return ["ai-handoff", f"agent:{task.assigned_agent}", f"priority:{task.priority}"]


if __name__ == "__main__":
    raise SystemExit(main())
