from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from .github_api import GitHubApiError, GitHubClient
from .models import RepositorySignal, StalledItem

SETUP_KEYWORDS = ("setup", "initial", "bootstrap", "api key", "secret", "deploy", "環境", "初期設定", "API", "認証")


def scan_repositories(client: GitHubClient, repos: list[str], stale_days: int) -> list[RepositorySignal]:
    return [scan_repository(client, repo, stale_days) for repo in repos]


def scan_repository(client: GitHubClient, repo: str, stale_days: int) -> RepositorySignal:
    warnings: list[str] = []
    source_url: str | None = f"https://github.com/{repo}"
    scanned_at = datetime.now(timezone.utc).isoformat()
    missing_readme = False
    missing_docs = False
    stale_issues: list[StalledItem] = []
    stale_pull_requests: list[StalledItem] = []
    failing_workflows: list[str] = []
    setup_keywords: list[str] = []

    try:
        repo_data = client.get_repo(repo)
        source_url = repo_data.get("html_url", source_url)
    except (GitHubApiError, ValueError) as exc:
        warnings.append(f"repo_metadata_unavailable: {exc}")

    try:
        client.get_readme(repo)
    except GitHubApiError:
        missing_readme = True

    try:
        client.get_contents(repo, "docs")
    except GitHubApiError:
        missing_docs = True

    cutoff = datetime.now(timezone.utc) - timedelta(days=stale_days)
    try:
        for item in client.list_open_issues_and_prs(repo):
            updated_at = parse_github_datetime(item.get("updated_at"))
            title = item.get("title", "Untitled")
            body = item.get("body") or ""
            if any(keyword.lower() in f"{title} {body}".lower() for keyword in SETUP_KEYWORDS):
                setup_keywords.append(title)
            if updated_at and updated_at <= cutoff:
                stalled = StalledItem(
                    number=int(item.get("number", 0)),
                    title=title,
                    url=item.get("html_url", source_url or ""),
                    updated_at=item.get("updated_at", ""),
                    kind="pull_request" if "pull_request" in item else "issue",
                )
                if stalled.kind == "pull_request":
                    stale_pull_requests.append(stalled)
                else:
                    stale_issues.append(stalled)
    except GitHubApiError as exc:
        warnings.append(f"issues_unavailable: {exc}")

    try:
        workflow_runs = client.list_workflow_runs(repo).get("workflow_runs", [])
        for run in workflow_runs[:10]:
            if run.get("conclusion") in {"failure", "timed_out", "cancelled"}:
                failing_workflows.append(run.get("html_url") or run.get("name") or "workflow failure")
    except GitHubApiError as exc:
        warnings.append(f"actions_unavailable: {exc}")

    return RepositorySignal(
        repo=repo,
        scanned_at=scanned_at,
        missing_readme=missing_readme,
        missing_docs=missing_docs,
        stale_issues=stale_issues,
        stale_pull_requests=stale_pull_requests,
        failing_workflows=failing_workflows,
        setup_keywords=dedupe(setup_keywords),
        warnings=warnings,
        source_url=source_url,
    )


def parse_github_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
