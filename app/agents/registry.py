from app.agents.tools.time_tool import TimeTool
from app.agents.tools.calculator_tool import CalculatorTool
from app.agents.tools.rag_tool import RagTool

def get_tools(ai_provider):

    return [
        TimeTool(),
        CalculatorTool(),
        RagTool(ai_provider),
    ]