from app.agents.response_prompt import build_response_prompt


class ResponseGenerator:
    def __init__(self, ai_provider):
        self.ai = ai_provider

    def generate(self, question, tool, tool_result):

        # if not tool.requires_llm_response:
        #     return tool_result

        prompt = build_response_prompt(question, tool.name, tool_result)

        return self.ai.chat([{"role": "user", "parts": [{"text": prompt}]}])
