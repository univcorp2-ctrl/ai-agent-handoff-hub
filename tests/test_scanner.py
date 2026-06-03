from __future__ import annotations

from datetime import datetime, timezone

from ai_agent_handoff_hub.scanner import parse_github_datetime


def test_parse_github_datetime() -> None:
    parsed = parse_github_datetime("2026-06-03T00:00:00Z")

    assert parsed == datetime(2026, 6, 3, 0, 0, tzinfo=timezone.utc)


def test_parse_github_datetime_returns_none_for_bad_value() -> None:
    assert parse_github_datetime("not-a-date") is None
    assert parse_github_datetime(None) is None
