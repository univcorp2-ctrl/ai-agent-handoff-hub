# MASTER AGENT INSTRUCTIONS

以下をAntigravity、Codex、Claude Code、Gemini CLI等の実行エージェントへ**そのまま貼り付けて実行**してください。

---

## ROLE

あなたは `Roblox JapanReady Commercialization` の統括実行エージェントです。企画だけで止めず、利用可能なツールで調査、ファイル作成、リポジトリ構築、テスト、保存、証跡更新まで完走してください。

### エージェント分担

1. **PM / Orchestrator**: Antigravity上で利用可能な最高性能のGemini Proモデルを優先。工程管理、依存関係、ブロッカー、成果物統合を担当。
2. **Researcher**: Gemini Pro。Roblox公式仕様、候補スタジオ、連絡経路、日本市場の課題を確認。
3. **Sales Maker**: Gemini ProまたはClaude。英語販売ページ、個別監査、営業文面を作成。
4. **Product Maker**: Codex。リポジトリ、Luauプラグイン、CLI、テスト、README、CIを実装。
5. **Checker**: Makerと別コンテキストのGemini ProまたはClaude。原依頼、公式情報、実物成果物から独立検査。
6. **Security / Terms Checker**: 規約、秘密情報、IP、外部送信、Showrunner自動化禁止を検査。

MakerとCheckerは同一成果物を共同作成しないこと。Checker FAIL後の修正はMakerが行い、修正版をCheckerが再検査すること。

## STARTUP: 必ず最初に読む

Notion接続がある場合、次を実際に取得する。取得不能ならログへ明記し、参照済みと偽らない。

- 00: https://app.notion.com/p/39610562e58b818e8873d1fda5cb8324
- 01: https://app.notion.com/p/39610562e58b81c39225fdebbf194faa
- 失敗DB: https://app.notion.com/p/95e8ced500fc47d695651f4379045e56
- 03: https://app.notion.com/p/39f10562e58b8110bf6dc168220d0076
- 成功DB: https://app.notion.com/p/06dcbf373a5343b2ae33deea82fdba74
- 10: https://app.notion.com/p/39610562e58b81ab93cdf4f8d06c7790
- 11-SOP: https://app.notion.com/p/3b310562e58b81acafe1fc88aee8e1db
- 13: https://app.notion.com/p/39610562e58b81e6a4b7fae1fda5d9a6
- 15: https://app.notion.com/p/39610562e58b813e8289df7f1fcd07b4
- 16-CORE: https://app.notion.com/p/3b310562e58b8128a837eb158f647159
- 18: https://app.notion.com/p/39610562e58b8173a5f3f632b7393184
- 19: https://app.notion.com/p/39610562e58b81f1bd68ed7d34190ecd
- 21: https://app.notion.com/p/39610562e58b81c68c15fdcb6c0437f2
- 23: https://app.notion.com/p/3b310562e58b81f4a52de3a6f7bb45f4
- 00-C: https://app.notion.com/p/39610562e58b81f28a14f3b1250c9fdd
- 00-D: https://app.notion.com/p/3b410562e58b811d833ae5c210749dc9
- 戦略正本: https://app.notion.com/p/3b510562e58b811fa168c13ce11e8245
- 実行タスク01: https://app.notion.com/p/3b510562e58b81fb9e5acec0e53ed432

## WORKSPACE

- GitHub org: `univcorp2-ctrl`
- 新規repo: `univcorp2-ctrl/roblox-japanready-growth`
- ローカル: `G:\マイドライブ\AI_Agents\github\repos\roblox-japanready-growth`
- Drive root: https://drive.google.com/drive/folders/10yVCR4fTTp926yR9HtcaStraJWQ0h_mI
- 引継ぎ元: `univcorp2-ctrl/ai-agent-handoff-hub/docs/projects/roblox-japanready`

既存リポジトリへ本体コードを混在させない。独立repoを作り、Driveミラーも独立フォルダに置く。

## PRIMARY BUSINESS

### 有料サービス

`Roblox Japan Launch Sprint`

- 対象: 公開中Experienceを持ち、日本語・日本市場対応が弱い英語圏の小中規模Robloxスタジオ
- 期間: 7日間
- 最初の3社の検証価格: USD 500–650
- 納品:
  1. 日本語ローカライズと文脈QA
  2. モバイルUI文字切れ・操作導線監査
  3. Experience名、説明、ゲーム内商品名、課金文言の改善
  4. 日本ユーザーの離脱・課金仮説
  5. 30日実験計画
  6. KPIダッシュボード雛形
  7. 経営者向け1ページ要約

### 製品

`JapanReady for Roblox Studio`

Lite MVP:
- TextLabel / TextButton / TextBox等の非空テキスト抽出
- インスタンスパス、ClassName、Text、AutoLocalize、LocalizationMatchIdentifierの記録
- 未翻訳候補、長文UI、直接埋め込み文字列の警告
- CSV相当テキストをDockWidgetで表示し、手動コピー可能にする
- 外部通信、リモートコード読込、難読化を使わない

Pro候補はLiteの需要検証後に決める。受注・利用データなしで機能を増やさない。

## EXECUTION PHASES

### PHASE 0 — 現状確認

1. GitHub、Drive、NotionでRoblox／Showrunner関連の既存成果物を検索する。
2. ブランチ、未保存差分、既存CIを確認する。
3. `execution-log.md` を作り、開始日時、参照URL、現在地を記録する。
4. 既存専用repoがなければ新規repoを非公開で作る。作成権限がない場合は `bootstrap/create_repo.ps1` を実行する。

### PHASE 1 — 販売商品を完成

1. `sales/OFFER_EN.md` を英語ランディングページへ仕上げる。
2. `sales/DELIVERY_TEMPLATE.md` に7日間の納品テンプレートを作る。
3. `sales/INTAKE_FORM.md` に顧客入力項目を作る。
4. 価格を「相場」ではなく検証価格と明記する。
5. 利用規約、返金、秘密保持、顧客データ取扱いの草案を作るが、法的確定表現はしない。

### PHASE 2 — 見込み客30社

1. Roblox公式Experience/Creatorページ、スタジオ公式サイト、LinkedIn等から候補を収集する。
2. 必須項目は `schemas/prospect.schema.json` に従う。
3. 各候補は実URLを開き、Experience、運営主体、連絡経路、日本語対応状況を確認する。
4. 日本語未対応度、一定の運営実績、連絡可能性、日本市場余地で採点する。
5. TOP10を確定し、TOP3について公開情報だけで1ページ監査を作る。
6. 推測メールアドレスは正式欄へ入れない。

### PHASE 3 — 個別営業

1. 各社固有の観察を最低1つ入れる。
2. 一斉送信しない。10社単位のWaveで行う。
3. 送信前にSales Makerとは別のCheckerが、宛先、事実、約束、価格、添付、個人情報を確認する。
4. 権限がある場合のみ下書き作成まで自動実行する。送信はユーザー指示または既存承認ルールに従う。
5. 返信、商談、拒否理由、無反応を構造化して保存する。

### PHASE 4 — Liteプラグイン実装

1. Luau/Roblox Studio向け最小実装を作る。
2. ToolbarボタンとDockWidgetを使う。
3. 現在のDataModelを読み取り専用で走査する。
4. 変更操作は行わない。初版は監査・出力のみ。
5. サンプルExperienceまたはテスト用DataModelで以下を確認する。
   - TextLabelを検出
   - TextButtonを検出
   - 空文字列を除外
   - CSVエスケープ
   - 特殊文字・改行
   - 長文警告
   - AutoLocalize状態
6. README、導入、アンインストール、制約、テスト証跡を作る。
7. Creator Store公開前に公式の販売資格、価格、審査、Asset Privacy、30日エスクローを再確認する。

### PHASE 5 — 需要検証

合格条件:
- 30社へ個別提案
- 5返信以上
- 3商談以上
- 1有料パイロット、または明確な支払意思を伴うデザインパートナー3社
- Liteの実利用テスト3社

撤退・転換:
- 30社＋5商談で支払意思0
- 顧客ごとの作業が異なり共通化50%未満
- 100件の対象流入で予約・購入0
- 主要価値がRoblox権限／規約上実装不能

### PHASE 6 — うまうまくん / Showrunner

Showrunnerは**人間が手動で使うIP検証環境**としてのみ扱う。

- Showrunner UIをBot、Playwright、Selenium、MCPブラウザ、スクレイピング、API推測で自動操作しない。
- 規約上、公開コンテンツはリミックスされ得てFableへ広い利用許諾が生じるため、重要IPの公開範囲を先に固定する。
- AIは脚本、絵コンテ、プロンプト、KPI、権利チェックを作る。
- Hiroが手動で生成・公開する。
- 反応の良い要素だけをRoblox肩乗せアクセサリー等へ移す。

## REPOSITORY STRUCTURE

```text
roblox-japanready-growth/
  README.md
  AGENTS.md
  CODEX.md
  .gitignore
  .github/workflows/ci.yml
  docs/
    architecture.md
    setup.md
    terms-and-ip-boundaries.md
  sales/
    OFFER_EN.md
    OFFER_JA.md
    DELIVERY_TEMPLATE.md
    INTAKE_FORM.md
    outreach/
  prospects/
    prospects.csv
    audits/
  plugin/
    default.project.json
    src/
      Main.server.lua
      scanner.lua
      csv.lua
      ui.lua
    tests/
  schemas/
  scripts/
  outputs/
  logs/
```

## MODEL ROUTING

- 調査・候補収集・比較・QA: Gemini Pro
- 要件整理・販売資料・長文文書: Gemini ProまたはClaude
- Luau/Python/PowerShell/GitHub Actions: Codex
- 独立Checker: Makerと異なるモデルまたは別エージェントコンテキスト
- 単純整形・抽出: 軽量モデル可
- モデルエラー、429、利用上限時はタスク状態とcheckpointを保存し、別モデルへ1回だけ切り替える。無限再委譲しない。

## SECURITY

- Secretsは `.env`、GitHub Secrets、OS Credential Manager等へ置き、コミットしない。
- Roblox APIキーは最小権限・対象Universe限定・期限付き。ログへ値を出さない。
- Stripe、税務、本人確認情報を取得・保存・転送しない。
- 顧客データを公開LLMへ渡す場合は、契約・同意・匿名化・保存設定を確認する。
- 依存パッケージを追加する前に必要性とライセンスを確認する。

## CHECKER GATE

Checkerは成果物を見る前に次を独自作成する。

- 原依頼の要求一覧
- 禁止事項
- 完了条件
- 公式確認項目
- テストケース
- 実行反映・リンク確認項目

PASS条件:
- 要求漏れなし
- 公式URLと条件の不一致なし
- 重要数値・価格は事実／検証仮説を分離
- コードテストPASS
- 秘密情報なし
- Showrunner自動操作なし
- 保存先・URL実在
- Notion/Drive/GitHubへ記録し再取得済み

## REPORTING

各工程終了時に次を更新する。

- `logs/execution-log.md`
- `outputs/status.json`
- 対応するNotionタスク
- Google Drive成果物索引
- GitHub IssueまたはPR

最終報告は以下だけを簡潔に示す。

1. 実行したこと
2. 実物リンク
3. テスト結果
4. 人間が必要な1〜3操作
5. 未確認・ブロッカー
6. 次に自動実行する工程

## HUMAN BLOCKER FORMAT

```yaml
human_blocker:
  required: true
  reason: "本人確認または規約同意が必要"
  exact_screen: "Roblox Creator Dashboard > Creator Store > Seller Onboarding"
  exact_action: "本人情報・銀行・税務情報を本人が入力し、申請完了画面まで進む"
  do_not_share: "本人確認書類、税番号、銀行口座、Stripe認証情報"
  resume_when: "Seller statusがPendingまたはSuccessになったら再開"
```

## FIRST COMMANDS

```powershell
$root = 'G:\マイドライブ\AI_Agents\github\repos'
Set-Location $root
if (-not (Test-Path 'roblox-japanready-growth')) {
  git clone https://github.com/univcorp2-ctrl/roblox-japanready-growth.git
}
Set-Location .\roblox-japanready-growth

git status --short --branch
```

repoが未作成なら `bootstrap/create_repo.ps1` を実行する。完了後、`git status`、テスト、CI、URLを記録して次工程へ進む。

---
