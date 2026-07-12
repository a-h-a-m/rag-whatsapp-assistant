from app.graph.state import AgentState


class AgentGraph:
    def __init__(
        self,
        tools,
        rag_graph,
        memory,
        selector,
        responder,
    ):
        self.tools = {
            tool.name: tool
            for tool in tools
        }
        self.rag_graph = rag_graph
        self.memory = memory
        self.selector = selector
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

    def create_tool_node(self, tool):
        def node(state: AgentState):
            state["tool_result"] = tool.run(
                state["decision"]["query"]
            )
            return state

        return node

    def run_rag(self, state: AgentState):
        rag_state = self.rag_graph.invoke(
            {
                "question": state["decision"]["query"],
                "history": state["history"],
            }
        )
        state["tool_result"] = rag_state["answer"]

        return state

    def unknown_tool(self, state: AgentState):
        state["tool_result"] = ""
        state["response"] = "I don't know how to answer that."

        return state

    def generate_response(self, state: AgentState):
        tool_name = state["decision"]["tool"]
        
        tool = None

        if tool_name in self.tools:
            tool = self.tools[tool_name]

        response = self.responder.generate(
            state["question"],
            tool,
            state["tool_result"],
        )

        state["response"] = response

        return state

    def route_tool(self, state: AgentState):
        tool_name = state["decision"]["tool"]

        if tool_name in self.tools:
            return tool_name

        return "unknown_tool"