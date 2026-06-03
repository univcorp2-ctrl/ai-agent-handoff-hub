from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


TRUE_VALUES = {"1", "true", "yes", "on", "y"}


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in TRUE_VALUES


@dataclass(frozen=True)
class AppConfig:
    github_token: str | None
    target_repos: list[str]
    stale_days: int
    output_dir: Path
    create_github_issues: bool
    dry_run: bool
    notion_token: str | None
    notion_database_id: str | None
    google_tasks_api_token: str | None
    google_tasks_tasklist_id: str | None
    google_tasks_webhook_url: str | None
    codex_command: str | None
    claude_code_command: str | None
    gemini_command: str | None

    @classmethod
    def from_env(
        cls,
        *,
        target_repos: str | None = None,
        stale_days: int | None = None,
        output_dir: str | None = None,
        dry_run: bool | None = None,
    ) -> "AppConfig":
        repos_raw = target_repos or os.getenv("TARGET_REPOS", "")
        repos = [repo.strip() for repo in repos_raw.split(",") if repo.strip()]
        return cls(
            github_token=os.getenv("GH_PAT") or os.getenv("GITHUB_TOKEN"),
            target_repos=repos,
            stale_days=stale_days or int(os.getenv("STALE_DAYS", "14")),
            output_dir=Path(output_dir or os.getenv("OUTPUT_DIR", "outputs")),
            create_github_issues=env_bool("AUTO_CREATE_GITHUB_ISSUES", False),
            dry_run=env_bool("DRY_RUN", False) if dry_run is None else dry_run,
            notion_token=os.getenv("NOTION_TOKEN"),
            notion_database_id=os.getenv("NOTION_DATABASE_ID"),
            google_tasks_api_token=os.getenv("GOOGLE_TASKS_API_TOKEN"),
            google_tasks_tasklist_id=os.getenv("GOOGLE_TASKS_TASKLIST_ID"),
            google_tasks_webhook_url=os.getenv("GOOGLE_TASKS_WEBHOOK_URL"),
            codex_command=os.getenv("CODEX_COMMAND"),
            claude_code_command=os.getenv("CLAUDE_CODE_COMMAND"),
            gemini_command=os.getenv("GEMINI_COMMAND"),
        )
