# Setup Guide

このプロジェクトの目的は、初期設定そのものをAIエージェントが進められる形にすることです。人間が必要になるのは、外部サービスの本人確認、最終承認、課金開始、利用規約同意、二段階認証など、機械が代行できない部分だけです。

## 1. GitHub連携

最初はGitHub Actionsの標準 `GITHUB_TOKEN` で現在のrepoをスキャンできます。複数repoを横断したい場合は `GH_PAT` をGitHub Secretsへ保存します。

推奨権限:

- Contents read
- Issues read/write
- Pull Requests read
- Actions read
- private repoを横断する場合は対象repoへのアクセス権

## 2. 対象リポジトリを指定

Workflow実行時の `target_repos` に以下の形式で入力します。

```text
owner/repo,owner/another-repo
```

指定しない場合は、このリポジトリ自身が対象になります。

## 3. Notion連携

必要なSecrets:

- `NOTION_TOKEN`
- `NOTION_DATABASE_ID`

Notion DBには最低限以下のプロパティを用意してください。

- `Name` title
- `Task ID` rich_text
- `Repo` rich_text
- `Agent` select
- `Priority` select
- `Status` select

## 4. Google To Do連携

2つの方式があります。

### API token方式

- `GOOGLE_TASKS_API_TOKEN`
- `GOOGLE_TASKS_TASKLIST_ID`

### Webhook方式

- `GOOGLE_TASKS_WEBHOOK_URL`

Zapier、Make、Cloudflare WorkerなどでGoogle To Doへ渡す場合はWebhook方式が簡単です。

## 5. GitHub Actions実行

Actionsタブから `AI Agent Handoff Hub` を実行します。

```text
target_repos: your-name/app-one,your-name/app-two
stale_days: 14
dry_run: true
```

`dry_run=true` では、外部同期とIssue作成は行わず、Artifactだけを生成します。本番同期する場合は `dry_run=false` にしてください。

## 6. 人間が必要な部分

AI側で完了できない可能性が高い操作:

- 外部サービスの本人確認
- 最終承認
- 課金開始
- 利用規約同意
- 二段階認証
- private repoへの権限付与

これらは `handoff-report.md` の `human_blocker` として明示されます。
