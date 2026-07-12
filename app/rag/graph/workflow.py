from langgraph.graph import END, START, StateGraph

from app.rag.graph.rag_graph import RAGGraph
from app.rag.graph.state import RAGState


def create_graph(
    provider,
    retriever,
    prompt_builder,
):
    rag_graph = RAGGraph(
        provider,
        retriever,
        prompt_builder,
    )

    builder = StateGraph(RAGState)

    builder.add_node("retrieve_contexts", rag_graph.retrieve_contexts)
    builder.add_node("build_prompt", rag_graph.build_prompt)
    builder.add_node("generate_answer", rag_graph.generate_answer)

    builder.add_edge(START, "retrieve_contexts")
    builder.add_edge("retrieve_contexts", "build_prompt")
    builder.add_edge("build_prompt", "generate_answer")
    builder.add_edge("generate_answer", END)

    return builder.compile()