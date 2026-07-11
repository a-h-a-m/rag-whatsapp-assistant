from app.agents.parser import parse_json
from app.agents.prompt import build_tool_prompt


class ToolSelector:
    def __init__(self, ai_provider, tools):
        self.ai = ai_provider
        self.tools = tools

    def select(self, question, history):

        formatted_history = self.format_history(history)

        prompt = build_tool_prompt(self.tools, question, formatted_history)

        response = self.ai.chat([{"role": "user", "parts": [{"text": prompt}]}])

        print("Raw LLM response:")
        print(response)

        return parse_json(response)

    def format_history(self, history):

        lines = []

        for item in history:
            lines.append(f"{item['role'].capitalize()}: {item['message']}")

        return "\n".join(lines)
