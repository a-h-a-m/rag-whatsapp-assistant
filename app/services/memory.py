from app.database.database import get_connection



def save_message(
    user_id,
    role,
    content
):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO messages
        (user_id, role, content)

        VALUES (?, ?, ?)
        """,

        (
            user_id,
            role,
            content
        )
    )


    conn.commit()
    conn.close()



def get_history(
    user_id,
    limit=10
):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT role, content

        FROM messages

        WHERE user_id = ?

        ORDER BY id DESC

        LIMIT ?
        """,

        (
            user_id,
            limit
        )
    )


    rows = cursor.fetchall()

    conn.close()


    return list(reversed(rows))