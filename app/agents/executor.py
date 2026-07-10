class ToolExecutor:

    def __init__(self, tools):
        self.tools = tools

    def execute(self, decision):

        tool = next(
            (
                t for t in self.tools
                if t.name == decision["tool"]
            ),
            None
        )

        if tool is None:
            result = ""
            # raise Exception(
            #     f"Unknown tool: {decision['tool']}"
            # )

        else:
            result = tool.run(
                decision["query"]
            )

        return tool, result