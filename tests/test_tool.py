from app.agents.tools.time_tool import TimeTool
from app.agents.tools.calculator_tool import CalculatorTool

time_tool = TimeTool()
calc_tool = CalculatorTool()

print(time_tool.run("What time is it?"))

print(calc_tool.run("25*48"))

print(calc_tool.run("(10+5)/3"))

print(calc_tool.run("abc"))