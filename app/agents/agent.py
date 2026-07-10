import json

from app.agents.selector import ToolSelector
from app.agents.executor import ToolExecutor
from app.agents.responder import ResponseGenerator
from app.agents.registry import get_tools
# from app.agents.prompt import build_tool_prompt
# from app.agents.parser import parse_json
# from app.agents.response_prompt import build_response_prompt
from app.agents.result import AgentResult

class Agent:

    def __init__(self, provider, memory):

        self.ai = provider
        self.memory = memory
        self.tools = get_tools(provider)

        self.selector = ToolSelector(
            provider,
            self.tools
        )

        self.executor = ToolExecutor(
            self.tools
        )

        self.responder = ResponseGenerator(
            provider
        )


    def run(self, chat_id, question):

        history = self.memory.get_recent_messages(
            chat_id,
            limit=10
        )

        decision = self.selector.select(
            question,
            history
        )

        tool, tool_result = self.executor.execute(
            decision
        )

        if tool is None:
            return AgentResult(
                tool="unknown",
                query=decision["query"],
                tool_result=tool_result,
                response="I don't know how to answer that."
            )

        response = self.responder.generate(
            question,
            tool,
            tool_result
        )
        
        return AgentResult(
            tool=tool.name,
            query=decision["query"],
            tool_result=tool_result,
            response=response
        )