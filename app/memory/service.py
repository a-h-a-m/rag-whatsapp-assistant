import sqlite3

from app.core.config import CHAT_HISTORY_DB


class MemoryService:
    def __init__(self, db_path=CHAT_HISTORY_DB):
        self.db = db_path

    def get_connection(self):
        return sqlite3.connect(self.db)

    def add_message(self, chat_id, role, message):

        conn = self.get_connection()

        conn.execute(
            """
            INSERT INTO messages
            (user_id, role, content)

            VALUES (?, ?, ?)
            """,
            (chat_id, role, message),
        )

        conn.commit()
        conn.close()

    def get_recent_messages(self, chat_id, limit=10):

        conn = self.get_connection()

        rows = conn.execute(
            """
            SELECT role, content

            FROM messages

            WHERE user_id = ?

            ORDER BY id DESC

            LIMIT ?
            """,
            (chat_id, limit),
        ).fetchall()

        conn.close()

        rows.reverse()

        return [{"role": role, "message": content} for role, content in rows]
