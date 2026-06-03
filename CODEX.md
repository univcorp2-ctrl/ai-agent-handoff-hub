# CODEX Instructions

このリポジトリでは、Codexは主に実装・修正・テスト・CI失敗修正を担当します。

## 実行方針

- 人間の確認を待たず、テストで検証できる範囲は自動で進める。
- 変更後は `pytest -q` と `ruff check .` を実行する。
- CI失敗時はログを読み、原因を特定し、修正して再実行する。
- Secretsの実値は絶対にコード、README、docsへ書かない。
- どうしても人間が必要な場合は `human_blocker` として理由を明記する。

## よく使うコマンド

```bash
pip install -e '.[dev]'
ruff check .
pytest -q
python -m ai_agent_handoff_hub run-all --target-repos owner/repo --output-dir outputs --dry-run
```

## 変更時に見る場所

- `src/ai_agent_handoff_hub/scanner.py`: GitHub検出ロジック
- `src/ai_agent_handoff_hub/planner.py`: AI割当・優先度ロジック
- `src/ai_agent_handoff_hub/reporting.py`: Artifact生成
- `.github/workflows/ai-agent-handoff.yml`: CI/CDと定期実行
- `docs/setup.md`: 初期設定の引き継ぎ手順
