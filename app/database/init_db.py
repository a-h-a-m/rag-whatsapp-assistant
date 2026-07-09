from app.database.database import get_connection


def init_database():

    conn = get_connection()

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