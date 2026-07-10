from app.agents.tool import Tool


class CalculatorTool(Tool):

    @property
    def name(self):
        return "calculator"

    @property
    def description(self):
        return (
            "Evaluates simple mathematical expressions "
            "such as addition, subtraction, multiplication, and division."
        )

    def run(self, query):

        try:
            # WARNING:
            # This uses eval() for simplicity.
            # We'll replace it with a safer parser later.
            result = eval(query)

            return str(result)

        except Exception:
            return "Invalid mathematical expression."