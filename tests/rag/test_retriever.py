from unittest.mock import MagicMock, patch

from app.rag.retriever import retrieve_context


def test_retrieve_context():
    embedding_provider = MagicMock()
    embedding_provider.embed.return_value = [0.1, 0.2, 0.3]

    collection = MagicMock()
    collection.query.return_value = {
        "documents": [[
            "Employee handbook",
            "Annual leave policy",
            "Remote work policy",
        ]]
    }

    with patch(
        "app.rag.retriever.get_collection",
        return_value=collection,
    ):

        result = retrieve_context(
            "leave",
            embedding_provider,
        )

    assert result == [
        "Employee handbook",
        "Annual leave policy",
        "Remote work policy",
    ]

def test_embedding_called_once():
    embedding_provider = MagicMock()
    embedding_provider.embed.return_value = [0.1, 0.2, 0.3]

    collection = MagicMock()
    collection.query.return_value = {
        "documents": [["Annual leave policy"]]
    }

    with patch(
        "app.rag.retriever.get_collection",
        return_value=collection,
    ):
        retrieve_context(
            "leave",
            embedding_provider,
        )

    embedding_provider.embed.assert_called_once_with(
        "leave"
    )

def test_collection_query_called():
    embedding_provider = MagicMock()
    embedding_provider.embed.return_value = [0.1, 0.2, 0.3]

    collection = MagicMock()
    collection.query.return_value = {
        "documents": [["Annual leave policy"]]
    }

    with patch(
        "app.rag.retriever.get_collection",
        return_value=collection,
    ):
        retrieve_context(
            "leave",
            embedding_provider,
        )

    collection.query.assert_called_once_with(
        query_embeddings=[[0.1, 0.2, 0.3]],
        n_results=3,
    )

def test_custom_limit():
    embedding_provider = MagicMock()
    embedding_provider.embed.return_value = [0.1, 0.2, 0.3]

    collection = MagicMock()
    collection.query.return_value = {
        "documents": [["Annual leave policy"]]
    }

    with patch(
        "app.rag.retriever.get_collection",
        return_value=collection,
    ):
        retrieve_context(
            "leave",
            embedding_provider,
            limit=5,
        )

    collection.query.assert_called_once_with(
        query_embeddings=[[0.1, 0.2, 0.3]],
        n_results=5,
    )

def test_empty_results():
    embedding_provider = MagicMock()
    embedding_provider.embed.return_value = [0.1, 0.2, 0.3]

    collection = MagicMock()
    collection.query.return_value = {
        "documents": [[]]
    }

    with patch(
        "app.rag.retriever.get_collection",
        return_value=collection,
    ):
        result = retrieve_context(
            "leave",
            embedding_provider,
        )

    assert result == []