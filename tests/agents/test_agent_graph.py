from unittest.mock import MagicMock, patch

# from app.providers.gemini.chat import GeminiProvider
from app.agents.agent import Agent

fake_rag_graph = MagicMock()
fake_rag_graph.invoke.return_value = {
    "answer": "Fake RAG answer",
}

class FakeMemory:
    def get_recent_messages(self, chat_id, limit=10):
        return []

    def add_message(self, *args, **kwargs):
        pass

class FakeHistoryMemory:
    def get_recent_messages(self, chat_id, limit=10):
        history = [
            {
                "role": "user",
                "message": "Hi",
            },
            {
                "role": "assistant",
                "message": "Hello!",
            },
        ]
        return history

    def add_message(self, *args, **kwargs):
        pass

class FakeAIProvider:
    def __init__(self, response):
        self.response = response

    def chat(self, prompt):
        return self.response

class FakeTool:
    name = "fake"
    description = "Fake tool for testing."
    # requires_llm_response = True

    def run(self, query):
        return f"received: {query}"

class FakeHistoryTool:
    name = "fake"
    description = "Fake tool for testing."
    # requires_llm_response = True

    def run(self, query):
        return "tool output"

def test_agent_selects_tool():
    provider = FakeAIProvider(
        """
        {
            "tool": "fake",
            "query": "hello"
        }
        """
    )

    with patch(
        "app.agents.agent.get_tools",
        return_value=[FakeTool()]
    ):
        agent = Agent(
            provider,
            FakeMemory(),
            fake_rag_graph
        )

        result = agent.run(
            "test-user",
            "say hello"
        )

    assert result.tool == "fake"
    assert result.query == "hello"

def test_agent_unknown_tool():
    provider = FakeAIProvider(
        """
        {
            "tool": "unknown",
            "query": "hello"
        }
        """
    )

    agent = Agent(
        provider,
        FakeMemory(),
        fake_rag_graph
    )

    # with patch.object(agent.executor, "execute", return_value=(None, "Unknown tool")):
    result = agent.run(
        "test-user",
        "do something impossible",
    )

    assert result.tool == "unknown"
    assert result.response == "I don't know how to answer that."

def test_agent_passes_history_to_selector():
    provider = FakeAIProvider(
        """
        {
            "tool": "fake",
            "query": "hello"
        }
        """
    )

    agent = Agent(
        provider,
        FakeHistoryMemory(),
        fake_rag_graph
    )

    history = [
        {
            "role": "user",
            "message": "Hi",
        },
        {
            "role": "assistant",
            "message": "Hello!",
        },
    ]

    with patch.object(agent.selector, "select") as mock_select:
        mock_select.return_value = {
            "tool": "fake",
            "query": "hello",
        }

        agent.run("test-user", "How are you?")

        mock_select.assert_called_once_with(
            "How are you?",
            history,
        )

def test_agent_calls_responder():
    provider = FakeAIProvider(
        """
        {
            "tool": "fake",
            "query": "hello"
        }
        """
    )

    with patch(
        "app.agents.agent.get_tools",
        return_value=[FakeHistoryTool()]
    ):
        agent = Agent(
            provider,
            FakeMemory(),
            fake_rag_graph
        )

        with patch.object(
            agent.responder, 
            "generate",
            return_value="I'm fine.",
        ) as mock_generate:
            agent.run("test-user", "How are you?")

            mock_generate.assert_called_once()

            args = mock_generate.call_args.args

            assert args[0] == "How are you?"
            assert isinstance(args[1], FakeHistoryTool)
            assert args[2] == "tool output"

def test_agent_returns_agent_result():
    provider = FakeAIProvider(
        """
        {
            "tool": "fake",
            "query": "hello"
        }
        """
    )

    with patch(
        "app.agents.agent.get_tools",
        return_value=[FakeHistoryTool()]
    ):
        agent = Agent(
            provider,
            FakeMemory(),
            fake_rag_graph
        )

        with patch.object(agent.responder, "generate", return_value="Hello!"):
            result = agent.run("test-user", "How are you?")

            assert result.tool == "fake"
            assert result.query == "hello"
            assert result.tool_result == "tool output"
            assert result.response == "Hello!"
    
def test_agent_uses_history_limit():
    provider = FakeAIProvider(
        """
        {
            "tool": "fake",
            "query": "hello"
        }
        """
    )

    memory = FakeMemory()

    with patch(
        "app.agents.agent.get_tools",
        return_value=[FakeTool()]
    ):
        agent = Agent(
            provider,
            memory,
            fake_rag_graph
        )

        with patch.object(
            memory, 
            "get_recent_messages",
            return_value=[],
        ) as mock_memory:
            agent.run("test-user", "How are you?")

            mock_memory.assert_called_once_with(
                "test-user",
                limit=10,
            )