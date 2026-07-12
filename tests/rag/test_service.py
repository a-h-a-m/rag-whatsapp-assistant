from unittest.mock import MagicMock, patch

from app.rag.service import RAGService


def test_answer_question():
    provider = MagicMock()
    retriever = MagicMock(
        return_value=["Annual leave policy"]
    )
    prompt_builder = MagicMock(
        return_value="Prompt"
    )
    rag = RAGService(
        provider,
        retriever,
        prompt_builder,
    )
    provider.chat.return_value = "Annual leave is 12 days."

    result = rag.answer_question(
        "How many annual leave days?",
    )

    assert result == "Annual leave is 12 days."

def test_retrieve_context_called():
    provider = MagicMock()
    retriever = MagicMock(
        return_value=["Context"]
    )
    prompt_builder = MagicMock(
        return_value="Prompt"
    )
    rag = RAGService(
        provider,
        retriever,
        prompt_builder,
    )
    provider.chat.return_value = "Answer"

    rag.answer_question(
        "How many annual leave days?",
    )

    retriever.assert_called_once_with(
        "How many annual leave days?",
        provider,
    )

def test_build_prompt_called():
    provider = MagicMock()
    contexts = [
        "Annual leave policy",
        "Remote work policy",
    ]
    retriever = MagicMock(
        return_value=contexts
    )
    prompt_builder = MagicMock(
        return_value="Prompt"
    )
    rag = RAGService(
        provider,
        retriever,
        prompt_builder,
    )
    provider.chat.return_value = "Answer"

    rag.answer_question(
        "How many annual leave days?",
    )

    prompt_builder.assert_called_once_with(
        contexts,
        "How many annual leave days?",
        None,
    )

def test_provider_called():
    provider = MagicMock()
    retriever = MagicMock(
        return_value=["Context"]
    )
    prompt_builder = MagicMock(
        return_value="Prompt"
    )
    rag = RAGService(
        provider,
        retriever,
        prompt_builder,
    )
    provider.chat.return_value = "Answer"

    rag.answer_question(
        "How many annual leave days?",
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
    retriever = MagicMock(
        return_value=["Context"]
    )
    prompt_builder = MagicMock(
        return_value="Prompt"
    )
    rag = RAGService(
        provider,
        retriever,
        prompt_builder,
    )
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

    rag.answer_question(
        "How many annual leave days?",
        history,
    )

    prompt_builder.assert_called_once_with(
        ["Context"],
        "How many annual leave days?",
        history,
    )

def test_empty_context():
    provider = MagicMock()
    retriever = MagicMock(
        return_value=[]
    )
    prompt_builder = MagicMock(
        return_value="Prompt"
    )
    rag = RAGService(
        provider,
        retriever,
        prompt_builder,
    )
    provider.chat.return_value = "I couldn't find any relevant information."

    result = rag.answer_question(
        "Unknown question",
    )

    prompt_builder.assert_called_once_with(
        [],
        "Unknown question",
        None,
    )

    provider.chat.assert_called_once()

    assert result == "I couldn't find any relevant information."