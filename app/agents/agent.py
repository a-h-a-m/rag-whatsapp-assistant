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
    def __init__(self, provider, memory):
        self.ai = provider
        self.memory = memory
        self.tools = get_tools(provider)

        self.selector = ToolSelector(provider, self.tools)

        self.executor = ToolExecutor(self.tools)

        self.responder = ResponseGenerator(provider)

        self.graph = create_graph(
            tools=self.tools,
            memory=self.memory,
            selector=self.selector,
            executor=self.executor,
            responder=self.responder,
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
            tool=state["tool_name"],
            query=state["decision"]["query"],
            tool_result=state["tool_result"],
            response=state["response"],
        )