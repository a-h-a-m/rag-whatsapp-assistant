from unittest.mock import MagicMock

from app.rag.graph.rag_graph import RAGGraph


def test_retrieve_contexts():
    provider = MagicMock()
    retriever = MagicMock(return_value=["Context"])
    prompt_builder = MagicMock()

    graph = RAGGraph(
        provider,
        retriever,
        prompt_builder,
    )

    state = {
        "question": "Leave?",
    }

    result = graph.retrieve_contexts(state)

    retriever.assert_called_once_with("Leave?", provider)

    assert result["contexts"] == ["Context"]

def test_build_prompt():
    provider = MagicMock()
    retriever = MagicMock()

    prompt_builder = MagicMock(
        return_value="Prompt"
    )

    graph = RAGGraph(
        provider,
        retriever,
        prompt_builder,
    )

    state = {
        "question": "Leave?",
        "contexts": ["Context"],
        "history": []
    }

    result = graph.build_prompt(state)

    prompt_builder.assert_called_once_with(
        ["Context"],
        "Leave?",
        []
    )

    assert result["prompt"] == "Prompt"

def test_generate_answer():
    provider = MagicMock()
    provider.chat.return_value = "Answer"

    graph = RAGGraph(
        provider,
        MagicMock(),
        MagicMock(),
    )

    state = {
        "prompt": "Prompt",
    }

    result = graph.generate_answer(state)

    provider.chat.assert_called_once_with(
        [
            {
                "role": "user",
                "parts": [
                    {
                        "text": "Prompt",
                    }
                ],
            }
        ]
    )

    assert result["answer"] == "Answer"