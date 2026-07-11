from app.agents.tools.calculator_tool import CalculatorTool
from app.agents.tools.rag_tool import RagTool
from app.agents.tools.time_tool import TimeTool


def get_tools(ai_provider):

    return [
        TimeTool(),
        CalculatorTool(),
        RagTool(ai_provider),
    ]
