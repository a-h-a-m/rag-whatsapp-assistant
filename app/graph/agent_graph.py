from app.graph.state import AgentState
from app.agents.utils import get_tool

class AgentGraph:
    def __init__(
        self,
        tools,
        memory,
        selector,
        executor,
        responder,
    ):
        self.tools = tools
        self.memory = memory
        self.selector = selector
        self.executor = executor
        self.responder = responder

    def load_history(self, state: AgentState):
        history = self.memory.get_recent_messages(
            state["chat_id"],
            limit=10,
        )

        state["history"] = history

        return state

    def select_tool(self, state: AgentState):
        decision = self.selector.select(
            state["question"],
            state["history"],
        )

        state["decision"] = decision

        return state

    def execute_tool(self, state: AgentState):
        tool, tool_result = self.executor.execute(
            state["decision"]
        )

        state["tool_name"] = "unknown" if not tool else tool.name
        state["tool_result"] = tool_result

        return state

    def unknown_tool(self, state: AgentState):
        state["response"] = "I don't know how to answer that."

        return state

    def generate_response(self, state: AgentState):
        tool = get_tool(self.tools, state["tool_name"])
        response = self.responder.generate(
            state["question"],
            tool,
            state["tool_result"],
        )

        state["response"] = response

        return state

    def route_after_execution(self, state: AgentState):
        tool = get_tool(self.tools, state["tool_name"])
        if tool is None:
            return "unknown_tool"

        return "generate_response"