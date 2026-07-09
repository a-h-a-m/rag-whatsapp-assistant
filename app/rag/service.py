from app.rag.retriever import retrieve_context
from app.rag.prompt import build_rag_prompt


def answer_question(
    question,
    ai_provider,
    history=None
):

    contexts = retrieve_context(
        question,
        ai_provider
    )

    prompt = build_rag_prompt(
        contexts,
        question,
        history
    )

    return ai_provider.chat(
        [
            {
                "role": "user",
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    )