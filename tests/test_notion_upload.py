from __future__ import annotations

from pathlib import Path

from ai_agent_handoff_hub.integrations.notion import NotionClient, build_multipart_body


def test_build_multipart_body_contains_file_and_part_number() -> None:
    body, content_type = build_multipart_body(
        b"png-bytes",
        filename="図解.png",
        content_type="image/png",
        part_number=2,
    )

    assert content_type.startswith("multipart/form-data; boundary=")
    assert b'name="file"' in body
    assert b"png-bytes" in body
    assert b'name="part_number"' in body
    assert b"\r\n2\r\n" in body


def test_upload_image_uses_direct_upload_and_verifies(tmp_path: Path, monkeypatch) -> None:
    image_path = tmp_path / "diagram.png"
    image_path.write_bytes(b"fake-png")
    calls: list[str] = []

    client = NotionClient("token", sleeper=lambda _: None)
    monkeypatch.setattr(client, "_get_workspace_file_limit", lambda: 5 * 1024 * 1024)

    def fake_create_file_upload(**kwargs):
        calls.append("create")
        assert kwargs["mode"] == "single_part"
        assert kwargs["content_type"] == "image/png"
        return {"id": "upload-id", "status": "pending"}

    def fake_send_file_upload(*args, **kwargs):
        calls.append("send")
        assert args[0] == "upload-id"

    def fake_append_image_block(*args, **kwargs):
        calls.append("append")
        assert args[0] == "page-id"
        assert args[1] == "upload-id"
        return {"id": "block-id", "type": "image"}

    monkeypatch.setattr(client, "_create_file_upload", fake_create_file_upload)
    monkeypatch.setattr(client, "_send_file_upload", fake_send_file_upload)
    monkeypatch.setattr(client, "_append_image_block", fake_append_image_block)
    monkeypatch.setattr(client, "_verify_image_block", lambda block_id: block_id == "block-id")

    result = client.upload_image("page-id", image_path, caption="図解")

    assert result.attached is True
    assert result.verified is True
    assert result.file_upload_id == "upload-id"
    assert result.block_id == "block-id"
    assert result.sha256 is not None
    assert calls == ["create", "send", "append"]


def test_upload_image_returns_clear_error_without_token(tmp_path: Path) -> None:
    image_path = tmp_path / "diagram.png"
    image_path.write_bytes(b"fake-png")

    result = NotionClient(None).upload_image("page-id", image_path)

    assert result.attached is False
    assert result.error == "NOTION_TOKEN is not configured"
