#!/usr/bin/env python3
"""Static release gate for the Roblox JapanReady handoff package.

This does not replace Luau lint/unit tests or a Roblox Studio smoke test. It
validates structure, JSON, prohibited code patterns, sales disclaimers, and
obvious secret leakage before those deeper tests run.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[4]

REQUIRED_FILES = [
    "README.md",
    "MASTER_AGENT_INSTRUCTIONS.md",
    "PROJECT_SPEC.md",
    "ACCEPTANCE_CRITERIA.md",
    "sales/OFFER_EN.md",
    "sales/OFFER_JA.md",
    "sales/DELIVERY_TEMPLATE.md",
    "sales/INTAKE_FORM.md",
    "schemas/prospect.schema.json",
    "bootstrap/create_repo.ps1",
    "prompts/ANTIGRAVITY_MASTER_PROMPT.md",
    "prompts/CODEX_BUILDER_PROMPT.md",
    "prompts/GEMINI_RESEARCH_SALES_PROMPT.md",
    "prompts/INDEPENDENT_CHECKER_PROMPT.md",
    "product/plugin/default.project.json",
    "product/plugin/src/Main.server.lua",
    "product/plugin/src/scanner.lua",
    "product/plugin/src/rules.lua",
    "product/plugin/src/csv.lua",
    "product/plugin/src/ui.lua",
    "product/plugin/tests/csv.spec.lua",
]

PLUGIN_SOURCE_FILES = [
    "product/plugin/src/Main.server.lua",
    "product/plugin/src/scanner.lua",
    "product/plugin/src/rules.lua",
    "product/plugin/src/csv.lua",
    "product/plugin/src/ui.lua",
]

FORBIDDEN_PLUGIN_PATTERNS: dict[str, re.Pattern[str]] = {
    "network URL": re.compile(r"https?://", re.IGNORECASE),
    "HttpService": re.compile(r"\bHttpService\b"),
    "HTTP request method": re.compile(
        r"\b(?:GetAsync|PostAsync|RequestAsync|HttpEnabled)\b"
    ),
    "remote numeric require": re.compile(r"\brequire\s*\(\s*\d+\s*\)"),
    "loadstring": re.compile(r"\bloadstring\b", re.IGNORECASE),
    "InsertService": re.compile(r"\bInsertService\b"),
    "AssetService": re.compile(r"\bAssetService\b"),
    "telemetry": re.compile(r"\btelemetry\b", re.IGNORECASE),
}

SECRET_PATTERNS: dict[str, re.Pattern[str]] = {
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "OpenAI-style secret": re.compile(r"\bsk-[A-Za-z0-9_-]{24,}\b"),
}


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)
    print(f"FAIL: {message}")


def check_json(path: Path, failures: list[str]) -> object | None:
    try:
        with path.open("r", encoding="utf-8") as file_handle:
            parsed = json.load(file_handle)
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"Invalid JSON in {path.relative_to(REPO_ROOT)}: {exc}", failures)
        return None
    print(f"PASS: JSON parses: {path.relative_to(REPO_ROOT)}")
    return parsed


def main() -> int:
    failures: list[str] = []

    for relative in REQUIRED_FILES:
        path = PACKAGE_ROOT / relative
        if not path.is_file():
            fail(f"Missing required file: {relative}", failures)
        else:
            print(f"PASS: required file exists: {relative}")

    schema = check_json(PACKAGE_ROOT / "schemas/prospect.schema.json", failures)
    project = check_json(PACKAGE_ROOT / "product/plugin/default.project.json", failures)

    if isinstance(schema, dict):
        required = set(schema.get("required", []))
        expected = {
            "prospect_id",
            "studio_name",
            "experience_name",
            "experience_url",
            "creator_url",
            "evidence_checked_at",
            "japanese_support_state",
            "observed_issue",
            "contact_verification",
            "fit_score",
            "priority",
            "outreach_status",
            "next_action",
        }
        missing = sorted(expected - required)
        if missing:
            fail(f"Prospect schema omits required fields: {missing}", failures)
        else:
            print("PASS: prospect schema has all mandatory evidence fields")

    if isinstance(project, dict):
        tree = project.get("tree", {})
        if tree.get("$className") != "Folder" or tree.get("$path") != "src":
            fail(
                "Rojo prototype must build a Folder model rooted at plugin/src",
                failures,
            )
        else:
            print("PASS: Rojo prototype is a model root, not ServerScriptService")

    for relative in PLUGIN_SOURCE_FILES:
        path = PACKAGE_ROOT / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for label, pattern in FORBIDDEN_PLUGIN_PATTERNS.items():
            if pattern.search(text):
                fail(f"{relative} contains prohibited {label}", failures)
        print(f"PASS: no prohibited network/remote-code pattern: {relative}")

    scanner_text = (PACKAGE_ROOT / "product/plugin/src/scanner.lua").read_text(
        encoding="utf-8"
    )
    scanner_mutations = re.compile(
        r"\.(?:Destroy|ClearAllChildren|SetAttribute|AddTag|RemoveTag)\s*\("
    )
    if scanner_mutations.search(scanner_text):
        fail("scanner.lua contains a mutating Instance operation", failures)
    else:
        print("PASS: scanner.lua contains no prohibited mutation method")

    all_text_parts: list[str] = []
    for path in PACKAGE_ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in {
            ".md",
            ".json",
            ".lua",
            ".py",
            ".ps1",
            ".yml",
            ".yaml",
        }:
            all_text_parts.append(path.read_text(encoding="utf-8", errors="replace"))
    all_text = "\n".join(all_text_parts)
    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(all_text):
            fail(f"Possible live {label} found in handoff package", failures)
        else:
            print(f"PASS: no obvious {label} detected")

    offer = (PACKAGE_ROOT / "sales/OFFER_EN.md").read_text(encoding="utf-8")
    required_offer_phrases = [
        "introductory validation price",
        "not a claim about an industry-wide market rate",
        "guaranteed increases",
        "without an API key",
    ]
    for phrase in required_offer_phrases:
        if phrase.lower() not in offer.lower():
            fail(f"English offer is missing required boundary: {phrase}", failures)
        else:
            print(f"PASS: offer boundary present: {phrase}")

    master = (PACKAGE_ROOT / "MASTER_AGENT_INSTRUCTIONS.md").read_text(
        encoding="utf-8"
    )
    if "Showrunner UIをBot" not in master or "MakerとChecker" not in master:
        fail("Master instructions omit Showrunner/manual or Maker–Checker gate", failures)
    else:
        print("PASS: master instructions contain Showrunner and Maker–Checker gates")

    if failures:
        print(f"\nSTATIC VALIDATION FAILED: {len(failures)} finding(s)")
        for index, message in enumerate(failures, start=1):
            print(f"{index}. {message}")
        return 1

    print("\nSTATIC VALIDATION PASSED")
    print(
        "NOTE: Luau lint/unit tests, PowerShell execution, Roblox Studio smoke "
        "testing, seller onboarding, and an independent agent review are still required."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
