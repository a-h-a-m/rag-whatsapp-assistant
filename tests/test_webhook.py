from unittest.mock import ANY, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_webhook_returns_200():
    with (
        patch(
            "app.routes.webhook.extract_message",
            return_value={
                "type": "textMessage",
                "text": "Hello",
                "chat_id": "123",
            },
        ),
        patch(
            "app.routes.webhook.handle_text_message",
        ),
    ):

        response = client.post(
            "/webhook",
            json={},
        )

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
    }

def test_text_message_calls_handler():
    with (
        patch(
            "app.routes.webhook.extract_message",
            return_value={
                "type": "textMessage",
                "text": "Hello",
                "chat_id": "123",
            },
        ),
        patch(
            "app.routes.webhook.handle_text_message",
        ) as mock_handle_text,
    ):

        client.post(
            "/webhook",
            json={},
        )

    mock_handle_text.assert_called_once_with(
        {
            "type": "textMessage",
            "text": "Hello",
            "chat_id": "123",
        },
        ANY,
        ANY,
    )

def test_audio_message_calls_audio_handler():
    with (
        patch(
            "app.routes.webhook.extract_message",
            return_value={
                "type": "audioMessage",
                "chat_id": "123",
            },
        ),
        patch(
            "app.routes.webhook.handle_audio_message",
            return_value="Hello from audio",
        ) as mock_handle_audio,
        patch(
            "app.routes.webhook.handle_text_message",
        ) as mock_handle_text,
    ):
        client.post(
            "/webhook",
            json={},
        )

    args, kwargs = mock_handle_audio.call_args

    assert args[0]["type"] == "audioMessage"
    assert args[0]["chat_id"] == "123"

    mock_handle_text.assert_called_once_with(
        {
            "type": "audioMessage",
            "text": "Hello from audio",
            "chat_id": "123",
        },
        ANY,
        ANY,
    )

def test_ignored_message():
    with (
        patch(
            "app.routes.webhook.extract_message",
            return_value={
                "type": "imageMessage",
            },
        ),
        patch(
            "app.routes.webhook.handle_audio_message",
        ) as mock_audio,
        patch(
            "app.routes.webhook.handle_text_message",
        ) as mock_text,
    ):

        response = client.post(
            "/webhook",
            json={},
        )

    assert response.status_code == 200
    assert response.json() == {
        "status": "ignored",
    }

    mock_audio.assert_not_called()
    mock_text.assert_not_called()

def test_extract_message_called():
    payload = {
        "typeWebhook": "incomingMessageReceived"
    }

    with patch(
        "app.routes.webhook.extract_message",
        return_value={
            "type": "imageMessage",
        },
    ) as mock_extract:

        client.post(
            "/webhook",
            json=payload,
        )

    mock_extract.assert_called_once_with(payload)

def test_invalid_payload():
    with patch(
        "app.routes.webhook.extract_message",
        side_effect=ValueError("Invalid payload"),
    ):

        response = client.post(
            "/webhook",
            json={},
        )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid payload",
    }