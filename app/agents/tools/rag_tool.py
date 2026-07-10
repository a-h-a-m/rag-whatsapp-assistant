from app.agents.tool import Tool
from app.rag.service import answer_question


class RagTool(Tool):

    def __init__(self, ai_provider):
        self.ai = ai_provider

    @property
    def name(self):
        return "rag"

    @property
    def description(self):
        return (
            "Answers questions using the company's knowledge base."
        )

    @property
    def requires_llm_response(self):
        return False
        
    def run(self, query):

        return answer_question(
            query,
            self.ai
        )