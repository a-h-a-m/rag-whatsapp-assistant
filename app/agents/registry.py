from app.agents.tools.calculator_tool import CalculatorTool
from app.agents.tools.time_tool import TimeTool

def get_tools():

    return [
        TimeTool(),
        CalculatorTool(),
    ]
