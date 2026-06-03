<p align="center">
  <img src="assets/hero.svg" alt="AIエージェント自動引き継ぎハブの全体アーキテクチャ" width="100%" />
</p>

# AI Agent Handoff Hub

止まっているGitHubリポジトリ、未完了Issue、放置PR、初期設定待ち、README未整備、CI失敗をAIエージェントが定期的に拾い、Codex / Claude Code / Gemini などの実行役へ渡せる形に分解し、Notion / Google To Do へ進捗を同期するための自動引き継ぎ基盤です。

このリポジトリは、最初から **README、docs、CI、テスト、devcontainer、定期実行Workflow、引き継ぎメモ、Secrets設計、成果物Artifact出力** まで入っています。人間が毎回確認ボタンを押す運用ではなく、AIが進められるところまで自動で進み、どうしても人間が必要な箇所だけを明示します。

<p align="center">
  <img src="assets/setup-guide.svg" alt="AIエージェント導入の初期設定ガイド" width="100%" />
</p>

## 何を自動化するか

| 領域 | 自動化する内容 | 人間が必要になりやすい部分 |
|---|---|---|
| GitHub監視 | 対象リポジトリ、Issue、PR、Actions、README、docs、未完了タスクを検出 | private repoへの権限付与 |
| AI引き継ぎ | タスク理解、優先度付け、Codex / Claude Code / Gemini への役割割当 | 最終方針の変更判断 |
| 初期設定 | Secrets名の一覧化、設定不足検出、依存関係、CI/CD、docs整備 | APIキー発行、本人確認、二段階認証 |
| 進捗同期 | Notion、Google To Do、Markdown、JSON Artifactへ同期 | 外部サービス初回認可 |
| 本番準備 | テスト、CI、ビルド、失敗ログ解析、次アクション作成 | 最終承認、課金開始、規約同意 |

## 最初に使うコマンド

Codespacesまたはdevcontainerで開いたら、次だけでローカル検証できます。

```bash
pip install -e '.[dev]'
python -m ai_agent_handoff_hub run-all --target-repos owner/repo --output-dir outputs
pytest -q
```

GitHub Actionsからは `AI Agent Handoff Hub` workflowを手動実行するか、定期実行を有効化してください。成果物は `ai-agent-handoff-report` Artifact として保存されます。

## GitHub Actionsでの本番運用

`.github/workflows/ai-agent-handoff.yml` は以下を行います。

1. 対象リポジトリをスキャン
2. 停滞・未完了・初期設定不足を検出
3. AI実行役に渡せるタスクへ分解
4. Markdown / JSON / Notion / Google To Do 用payloadを生成
5. 必要に応じてGitHub Issueを自動作成
6. Artifactへ引き継ぎ資料を保存

### 推奨Secrets

Secretsの実値はREADMEやコードに絶対に書かず、GitHub Secrets / Cloudflare Secrets / 利用する実行基盤のSecretsに保存してください。

| Secret名 | 用途 | 必須 |
|---|---|---|
| `GH_PAT` | 複数リポジトリを横断して読む/Issue作成するためのGitHub token | 推奨 |
| `NOTION_TOKEN` | Notion API連携 | 任意 |
| `NOTION_DATABASE_ID` | タスク同期先Notion DB | 任意 |
| `GOOGLE_TASKS_API_TOKEN` | Google Tasks API連携用アクセストークン | 任意 |
| `GOOGLE_TASKS_TASKLIST_ID` | Google To Do / Tasks の同期先リストID | 任意 |
| `GOOGLE_TASKS_WEBHOOK_URL` | Google Tasks連携を外部自動化に委譲する場合のWebhook | 任意 |
| `CODEX_COMMAND` | CodexをCLI実行する場合のコマンド | 任意 |
| `CLAUDE_CODE_COMMAND` | Claude CodeをCLI実行する場合のコマンド | 任意 |
| `GEMINI_COMMAND` | GeminiをCLI実行する場合のコマンド | 任意 |

## 自動で残す成果物

実行ごとに `outputs/` に以下を残します。

- `handoff-report.json`: 検出結果、タスク、担当AI、優先度、人間が必要な理由
- `handoff-report.md`: AI同士が読みやすい引き継ぎメモ
- `notion-payload.json`: Notion同期用payload
- `google-tasks-payload.json`: Google To Do同期用payload
- `agent-commands.md`: Codex / Claude Code / Gemini に渡す実行指示

## AI実行役の基本方針

| Agent | 担当 | 例 |
|---|---|---|
| Codex | 実装、修正、テスト、CI失敗修正 | failing workflow、バグ修正、テスト追加 |
| Claude Code | 設計、整理、ドキュメント、要件分解 | README、setup.md、architecture.md、初期設定手順 |
| Gemini | 調査、検証、QA、比較 | 外部API調査、ログ検証、再現確認 |

## 人間の確認を挟まないための設計

このリポジトリは「AIが安全に進められる範囲」を広く取り、以下を自動化します。

- CIで検証できる変更はAI側で再実行まで行う
- 失敗時はログを解析し、次のAIが再開できるメモを残す
- Secretsの実値は扱わず、必要なSecret名だけを明示する
- 外部サービスの本人確認、最終承認、課金開始、規約同意、二段階認証だけを人間タスクとして残す

## アーキテクチャ

```mermaid
flowchart LR
  G[GitHub Repos / Issues / PRs / Actions] --> S[Scanner]
  S --> P[Planner]
  P --> A[Agent Assignment]
  A --> C[Codex]
  A --> CC[Claude Code]
  A --> GM[Gemini]
  P --> R[Reports]
  R --> N[Notion]
  R --> T[Google To Do]
  R --> I[GitHub Issues]
  R --> H[Handoff Memo]
```

詳細は [`docs/architecture.md`](docs/architecture.md) と [`docs/setup.md`](docs/setup.md) を見てください。

## 現在の完成状態

- Python CLI実装済み
- GitHub API scanner実装済み
- タスク分解planner実装済み
- Notion / Google To Do payload生成実装済み
- GitHub Issue作成オプション実装済み
- README先頭用画像SVG同梱済み
- CI / テスト / devcontainer / docs同梱済み

## 未完了として残る可能性があるもの

実値が必要な外部サービス認証は、人間または別AIエージェントに渡す必要があります。この場合も `outputs/handoff-report.md` に、何が未完了で、どのSecretが必要で、次に何をするかを自動で残します。
