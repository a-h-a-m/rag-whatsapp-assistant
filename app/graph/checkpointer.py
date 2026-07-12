# from pathlib import Path

from langgraph.checkpoint.memory import InMemorySaver

# from langgraph.checkpoint.sqlite import SqliteSaver

# DATA_DIR = Path("data")
# DATA_DIR.mkdir(exist_ok=True)

# DB_PATH = DATA_DIR / "graph.db"

# checkpointer = SqliteSaver.from_conn_string(
#     str(DB_PATH),
# )
checkpointer = InMemorySaver()