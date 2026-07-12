from app.rag.graph.workflow import create_graph
from app.rag.prompt import build_rag_prompt
from app.rag.retriever import retrieve_context

class RAGService:
    def __init__(
        self,
        provider,
        retriever=retrieve_context,
        prompt_builder=build_rag_prompt,
    ):
        self.graph = create_graph(
            provider,
            retriever,
            prompt_builder,
        )

    def answer_question(self, question, history=None):
        state = self.graph.invoke(
            {
                "question": question,
                "history": history
            }
        )

        return state["answer"]

    # def answer_question(question, ai_provider, history=None):
    #     contexts = retrieve_context(question, ai_provider)

    #     prompt = build_rag_prompt(contexts, question, history)

    #     return ai_provider.chat([{"role": "user", "parts": [{"text": prompt}]}])
