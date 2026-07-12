# from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from app.graph.agent_graph import AgentGraph
from app.graph.state import AgentState

def create_graph(
    tools,
    rag_graph,
    memory, 
    selector,
    responder,
    *,
    checkpointer=None
):
    # checkpointer = InMemorySaver()

    graph = AgentGraph(
        tools,
        rag_graph,
        memory,
        selector,
        responder,
    )

    builder = StateGraph(AgentState)

    builder.add_node("load_history", graph.load_history)
    builder.add_node("select_tool", graph.select_tool)
    
    for tool in tools:
        builder.add_node(
            tool.name,
            graph.create_tool_node(tool),
        )

        builder.add_edge(
            tool.name,
            "generate_response"
        )

    builder.add_node("rag", graph.run_rag)
    builder.add_node("generate_response", graph.generate_response)
    builder.add_node("unknown_tool", graph.unknown_tool)

    builder.add_edge(START, "load_history")
    builder.add_edge("load_history", "select_tool")
    
    builder.add_conditional_edges(
        "select_tool",
        graph.route_tool,
    )

    builder.add_edge("rag", "generate_response")
    builder.add_edge("generate_response", END)
    builder.add_edge("unknown_tool", END)

    return builder.compile(
        checkpointer=checkpointer,
    )