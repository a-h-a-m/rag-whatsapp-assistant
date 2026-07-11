from datetime import datetime

from app.agents.tool import Tool


class TimeTool(Tool):
    @property
    def name(self):
        return "time"

    @property
    def description(self):
        return "Returns the current local time."

    def run(self, query):

        now = datetime.now()

        return now.strftime("%H:%M:%S")
