from app.core.config import CHAT_HISTORY_DB
from app.database.database import get_connection


def init_database(db_path=CHAT_HISTORY_DB):

    conn = get_connection(db_path)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id TEXT NOT NULL,

            role TEXT NOT NULL,

            content TEXT NOT NULL,

            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()

    conn.close()


if __name__ == "__main__":
    init_database()
