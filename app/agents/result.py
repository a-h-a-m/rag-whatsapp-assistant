from dataclasses import dataclass


@dataclass
class AgentResult:

    tool: str

    query: str

    tool_result: str

    response: str