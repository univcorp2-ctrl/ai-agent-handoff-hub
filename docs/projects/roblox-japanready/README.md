# Roblox JapanReady Commercialization

このディレクトリは、Roblox／Showrunner系の新興クリエイター経済へ参入するための、**販売検証 → 顧客学習 → Roblox Studioプラグイン製品化 → うまうまくんIP検証**の引き継ぎパッケージです。

## 最重要ゴール

最初から大型ゲームを作らず、英語圏Robloxスタジオに次の商品を販売して、実際の支払意思を検証します。

**商品:** Roblox Japan Launch Sprint  
**検証価格:** 最初の3社は USD 500–650  
**期間:** 7日間  
**初期KPI:** 30社へ個別提案、5返信、3商談、1有料パイロット

## 実行順

1. `MASTER_AGENT_INSTRUCTIONS.md` を実行エージェントへそのまま渡す。
2. `PROJECT_SPEC.md` と `ACCEPTANCE_CRITERIA.md` を読み、完了条件を固定する。
3. `sales/OFFER_EN.md` を販売ページ・個別提案の正本として使う。
4. 30社の候補を `schemas/prospect.schema.json` に準拠して作る。
5. 有料または深掘りサンプルの実作業から、反復工程を `product/` のLiteプラグインへ移す。
6. MakerとCheckerを分離し、Checker PASS前に公開・送信・本番反映しない。

## 推奨新規リポジトリ

後続エージェントは、次の独立リポジトリを作成してください。

- GitHub: `univcorp2-ctrl/roblox-japanready-growth`
- ローカル: `G:\マイドライブ\AI_Agents\github\repos\roblox-japanready-growth`
- Google Drive正本: `Roblox_Showrunner_Commercialization`

このハブ内のファイルは引き継ぎ正本です。実装コードは上記の独立リポジトリへ移し、既存リポジトリを壊さないでください。

## 人間が必要な箇所

AIは調査、候補抽出、資料作成、コード、テスト、ログ更新まで進めます。Hiro本人が必要なのは原則として次だけです。

- Robloxへのログイン、本人確認、Seller Onboarding、Stripe・税務情報の入力
- 外部送信または価格・契約・公開の最終承認
- Roblox Studioの初回認証が必要な場合のログイン
- うまうまくんの重要IPを公開する範囲の承認

## 公式仕様の入口

- Creator Store: https://create.roblox.com/docs/production/creator-store
- Studio plugins: https://create.roblox.com/docs/studio/plugins
- Localization: https://create.roblox.com/docs/production/localization
- Analytics Query API: https://create.roblox.com/docs/cloud/guides/analytics
- Open Cloud: https://create.roblox.com/docs/cloud
- Showrunner Terms: https://www.showrunner.xyz/termsofservice

## 禁止事項

- ShowrunnerへブラウザBot、スクレイパー、自動生成スクリプトでアクセスしない。
- 無許諾のNike、Disney、アニメ、著名人、音声、ロゴ、キャラクターを使わない。
- APIキー、Cookie、Stripe情報、税務情報をGitHub・Drive・Notionへ保存しない。
- 見込み客へ同一文面を大量送信しない。必ず各ゲーム固有の観察を1つ以上入れる。
- 受注前に大型UEFN島、Roblox大型ゲーム、広告費へ先行投資しない。
