# Copy-paste prompt for Codex

```text
You are the implementation Maker for `univcorp2-ctrl/roblox-japanready-growth`.

Read first:
- AGENTS.md and CODEX.md in the target repo
- Handoff package: https://github.com/univcorp2-ctrl/ai-agent-handoff-hub/tree/feature/roblox-japanready-bootstrap/docs/projects/roblox-japanready
- PROJECT_SPEC.md
- ACCEPTANCE_CRITERIA.md

Your scope is the JapanReady Lite v0.1 Roblox Studio plugin and its deterministic test/tooling scaffold. Do not design the business again and do not expand into Pro features.

Required behavior:
1. A toolbar button opens a DockWidget.
2. A read-only scan finds non-empty TextLabel, TextButton, and TextBox text in the current DataModel.
3. Findings contain instance path, class, name, text, Unicode length, AutoLocalize, LocalizationMatchIdentifier where readable, and warning codes.
4. The plugin shows CSV-safe output in a selectable text area for manual copy.
5. No object is modified.
6. No remote code, require(assetId), loadstring, InsertService/AssetService remote loading, HTTP request, telemetry, external billing, obfuscation, or secret is used.
7. Domain logic is separated from UI.
8. The tool fails safely and reports that no object was changed.

Before implementation:
- Inspect repository status and existing files.
- Verify current official Roblox plugin APIs and current Rojo/Luau tooling from primary documentation.
- Record exact versions and links in docs/setup.md. Do not invent versions.

Implement:
- plugin/src/scanner.lua
- plugin/src/rules.lua
- plugin/src/csv.lua
- plugin/src/ui.lua
- plugin/src/Main.server.lua
- plugin/tests/*
- plugin/default.project.json or the current verified equivalent
- README install/use/privacy/uninstall/limits
- CI/lint/test configuration that can run outside Studio where possible

Tests must cover plain text, empty text, comma, quote, newline, Japanese Unicode, long-text boundary, AutoLocalize state, ignored objects, duplicate text at different paths, and failure handling.

Validation:
- Run formatting/lint/tests and save complete commands/results.
- Create a small Studio smoke-test checklist. If you can operate Studio, execute it; otherwise create a precise human blocker with exact screens and expected output, while completing all non-Studio tests.
- Search the repository and git diff for secret-like values.
- Freeze the Maker artifact and hand it to a separate Checker. Do not self-approve.

Update:
- logs/execution-log.md
- outputs/status.json
- README and docs
- corresponding Notion task and Drive index if connectors are available

Do not publish to Creator Store and do not merge to main until the independent Checker passes.
```
