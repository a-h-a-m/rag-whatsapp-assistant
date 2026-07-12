from typing import TypedDict


class RAGState(TypedDict):

    question: str
    history: list

    contexts: list[str]

    prompt: str

    answer: str