from unittest.mock import MagicMock, patch

from app.rag.service import answer_question


def test_answer_question():
    provider = MagicMock()
    provider.chat.return_value = "Annual leave is 12 days."

    with (
        patch(
            "app.rag.service.retrieve_context",
            return_value=["Annual leave policy"],
        ),
        patch(
            "app.rag.service.build_rag_prompt",
            return_value="Prompt",
        ),
    ):

        result = answer_question(
            "How many annual leave days?",
            provider,
        )

    assert result == "Annual leave is 12 days."

def test_retrieve_context_called():
    provider = MagicMock()
    provider.chat.return_value = "Answer"

    with (
        patch(
            "app.rag.service.retrieve_context",
            return_value=["Context"],
        ) as mock_retrieve,
        patch(
            "app.rag.service.build_rag_prompt",
            return_value="Prompt",
        ),
    ):

        answer_question(
            "How many annual leave days?",
            provider,
        )

    mock_retrieve.assert_called_once_with(
        "How many annual leave days?",
        provider,
    )

def test_build_prompt_called():
    provider = MagicMock()
    provider.chat.return_value = "Answer"

    contexts = [
        "Annual leave policy",
        "Remote work policy",
    ]

    with (
        patch(
            "app.rag.service.retrieve_context",
            return_value=contexts,
        ),
        patch(
            "app.rag.service.build_rag_prompt",
            return_value="Prompt",
        ) as mock_prompt,
    ):

        answer_question(
            "How many annual leave days?",
            provider,
        )

    mock_prompt.assert_called_once_with(
        contexts,
        "How many annual leave days?",
        None,
    )

def test_provider_called():
    provider = MagicMock()
    provider.chat.return_value = "Answer"

    with (
        patch(
            "app.rag.service.retrieve_context",
            return_value=["Context"],
        ),
        patch(
            "app.rag.service.build_rag_prompt",
            return_value="Prompt",
        ),
    ):

        answer_question(
            "How many annual leave days?",
            provider,
        )

    provider.chat.assert_called_once_with(
        [
            {
                "role": "user",
                "parts": [
                    {
                        "text": "Prompt"
                    }
                ]
            }
        ]
    )

def test_history_passed():
    provider = MagicMock()
    provider.chat.return_value = "Answer"

    history = [
        {
            "role": "user",
            "message": "Hello",
        },
        {
            "role": "assistant",
            "message": "Hi!",
        },
    ]

    with (
        patch(
            "app.rag.service.retrieve_context",
            return_value=["Context"],
        ),
        patch(
            "app.rag.service.build_rag_prompt",
            return_value="Prompt",
        ) as mock_prompt,
    ):

        answer_question(
            "How many annual leave days?",
            provider,
            history,
        )

    mock_prompt.assert_called_once_with(
        ["Context"],
        "How many annual leave days?",
        history,
    )

def test_empty_context():
    provider = MagicMock()
    provider.chat.return_value = "I couldn't find any relevant information."

    with (
        patch(
            "app.rag.service.retrieve_context",
            return_value=[],
        ),
        patch(
            "app.rag.service.build_rag_prompt",
            return_value="Prompt",
        ) as mock_prompt,
    ):

        result = answer_question(
            "Unknown question",
            provider,
        )

    mock_prompt.assert_called_once_with(
        [],
        "Unknown question",
        None,
    )

    provider.chat.assert_called_once()

    assert result == "I couldn't find any relevant information."