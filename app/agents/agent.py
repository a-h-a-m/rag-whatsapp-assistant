from app.agents.executor import ToolExecutor
from app.agents.registry import get_tools
from app.agents.responder import ResponseGenerator

# from app.agents.prompt import build_tool_prompt
# from app.agents.parser import parse_json
# from app.agents.response_prompt import build_response_prompt
from app.agents.result import AgentResult
from app.agents.selector import ToolSelector
from app.graph.workflow import create_graph


class Agent:
    def __init__(
        self, 
        provider, 
        memory, 
        rag_graph,
        checkpointer=None
    ):
        self.ai = provider
        self.memory = memory
        self.tools = get_tools()

        self.selector = ToolSelector(provider, self.tools)

        self.responder = ResponseGenerator(provider)

        self.graph = create_graph(
            tools=self.tools,
            rag_graph=rag_graph,
            memory=self.memory,
            selector=self.selector,
            responder=self.responder,
            checkpointer=checkpointer
        )

    def run(self, chat_id, question):
        state = self.graph.invoke(
            {
                "chat_id": chat_id,
                "question": question,
            },
            config={
                "configurable": {
                    "thread_id": chat_id,
                }
            },
        )

        return AgentResult(
            tool=state["decision"]["tool"],
            query=state["decision"]["query"],
            tool_result=state["tool_result"],
            response=state["response"],
        )