from app.rag.graph.state import RAGState


class RAGGraph:
    def __init__(
        self,
        provider,
        retriever,
        prompt_builder,
    ):
        self.provider = provider
        self.retriever = retriever
        self.prompt_builder = prompt_builder

    def retrieve_contexts(
        self,
        state: RAGState,
    ):
        contexts = self.retriever(
            state["question"],
            self.provider,
        )

        state["contexts"] = contexts

        return state

    def build_prompt(
        self,
        state: RAGState,
    ):
        prompt = self.prompt_builder(
            state["contexts"],
            state["question"],
            state["history"]
        )

        state["prompt"] = prompt

        return state

    def generate_answer(
        self,
        state: RAGState,
    ):
        answer = self.provider.chat(
            [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": state["prompt"],
                        }
                    ],
                }
            ]
        )

        state["answer"] = answer

        return state