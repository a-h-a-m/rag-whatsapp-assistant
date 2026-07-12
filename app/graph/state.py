from typing import Any, TypedDict


class AgentState(TypedDict):
    chat_id: str
    question: str

    history: list

    decision: dict[str, Any]

    tool_name: str

    tool_result: Any | None

    response: str | None