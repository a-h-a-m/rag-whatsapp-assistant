from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from app.graph.agent_graph import AgentGraph
from app.graph.state import AgentState


def create_graph(
    tools,
    memory, 
    selector,
    executor,
    responder,
):
    checkpointer = InMemorySaver()

    graph = AgentGraph(
        tools,
        memory,
        selector,
        executor,
        responder,
    )

    builder = StateGraph(AgentState)

    builder.add_node("load_history", graph.load_history)
    builder.add_node("select_tool", graph.select_tool)
    builder.add_node("execute_tool", graph.execute_tool)
    builder.add_node("generate_response", graph.generate_response)
    builder.add_node("unknown_tool", graph.unknown_tool)

    builder.add_edge(START, "load_history")
    builder.add_edge("load_history", "select_tool")
    builder.add_edge("select_tool", "execute_tool")
    
    builder.add_conditional_edges(
        "execute_tool",
        graph.route_after_execution,
    )

    builder.add_edge("generate_response", END)
    builder.add_edge("unknown_tool", END)

    return builder.compile(
        checkpointer=checkpointer,
    )