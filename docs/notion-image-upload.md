# Notion画像アップロード共通標準

## 目的

Notionへの画像保存を、Google Driveの閲覧URLや一時URLに依存せず、Notion公式File Upload APIで確実に実行します。

この手順は、調査レポート、生成画像、図解、スクリーンショット、チャートなど、すべてのNotion画像保存処理に共通適用します。

## 絶対ルール

1. Google Driveの`/view` URLをNotion画像URLとして使わない。
2. ローカルファイルパスをNotionの外部画像URLとして渡さない。
3. Notion公式File Upload APIで画像本体をアップロードする。
4. アップロード後、1時間以内にページまたはブロックへ添付する。
5. 画像ブロックを再取得して存在を確認するまで、処理を成功扱いにしない。
6. 認証情報、APIレスポンスの署名付きURL、Refresh Tokenをログへ出さない。

## 必要な設定

GitHub Secretsまたは実行環境へ次を設定します。

```text
NOTION_TOKEN=secret_xxx
```

対象ページはNotion Integrationへ共有し、Integrationにページ内容を挿入できる権限を付与してください。

## 標準コマンド

```bash
python -m ai_agent_handoff_hub upload-notion-image \
  --page-id "NOTION_PAGE_ID" \
  --file "/absolute/path/to/image.png" \
  --caption "図解の説明"
```

成功時は、次のようなJSONを返します。

```json
{
  "attached": true,
  "file_upload_id": "...",
  "block_id": "...",
  "verified": true,
  "sha256": "...",
  "size_bytes": 123456,
  "content_type": "image/png",
  "error": null
}
```

`attached=true`かつ`verified=true`のときだけ完了です。

## 内部処理

```text
ローカル画像
  ↓ ファイル存在・MIME・サイズ検証
Notion File Upload作成
  ↓
画像本体をmultipart/form-dataで送信
  ↓ 20MB超なら分割アップロードを完了
Notionページへimageブロックを追加
  ↓
追加したimageブロックを再取得
  ↓
verified=trueで完了
```

## 容量と形式

- 20MB以下: single-part upload
- 20MB超: multi-part upload
- 実際の上限は`GET /v1/users/me`の`workspace_limits.max_file_upload_size_in_bytes`で事前確認
- 対応形式: PNG、JPEG、GIF、WebP、SVG、TIFF、HEIC、BMP、AVIF、APNG、ICOなど
- 空ファイル、未対応MIME、ワークスペース上限超過は送信前に停止

## 再試行

次の一時的エラーは指数バックオフで再試行します。

- HTTP 429
- HTTP 500
- HTTP 503
- HTTP 504
- HTTP 529
- 一時的なネットワークエラー

認証エラー、権限不足、ファイル形式不正、容量超過は自動再試行せず、原因を明示して停止します。

## 失敗時の確認順序

1. `NOTION_TOKEN`が設定されているか
2. 対象ページがIntegrationへ共有されているか
3. Integrationに挿入権限があるか
4. ファイルが実在し、空でないか
5. MIMEタイプが画像として認識されるか
6. ワークスペースのファイル上限を超えていないか
7. File Upload作成が成功したか
8. 画像データ送信が成功したか
9. 画像ブロック追加が成功したか
10. ブロック再取得で`type=image`を確認できたか

## 禁止する旧方式

以下は不安定なため、原則使用禁止です。

```text
ローカル画像 → Google Driveへ保存 → /view URLをNotionへ埋め込む
```

Google Driveの閲覧URLは画像データそのものではなく、認証やリダイレクトを伴う閲覧ページです。Notion側サーバーから画像本体を取得できず、リンクだけ残る、表示されない、期限切れになる、といった失敗につながります。

外部URL方式を例外的に使う場合は、認証不要・リダイレクトなし・HTTPS・画像本体を直接返すURLであることを事前検証してください。

## 完了判定

処理完了ログには最低限、次を残します。

```text
notion_image_upload: PASS | FAIL
file_upload_created: PASS | FAIL
file_bytes_sent: PASS | FAIL
image_block_appended: PASS | FAIL
image_block_refetched: PASS | FAIL
sha256: <digest>
size_bytes: <number>
content_type: <mime>
error: <redacted message or null>
```

File Upload IDやBlock IDは運用ログへ残せますが、トークンや一時的な署名付きURLは保存しません。
