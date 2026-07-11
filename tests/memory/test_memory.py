import sqlite3

from app.database.init_db import init_database
from app.memory.service import MemoryService


def test_save_user_message(tmp_path):
    db = tmp_path / "chat.db"

    init_database(str(db))

    memory = MemoryService(str(db))

    memory.add_message(
        "user-1",
        "user",
        "Hello!"
    )

    conn = sqlite3.connect(db)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, role, content
        FROM messages
    """)

    row = cursor.fetchone()

    conn.close()

    assert row == (
        "user-1",
        "user",
        "Hello!"
    )

def test_save_assistant_message(tmp_path):
    db = tmp_path / "chat.db"

    init_database(str(db))

    memory = MemoryService(str(db))

    memory.add_message(
        "user-1",
        "assistant",
        "Hello, how can I help you?"
    )

    conn = sqlite3.connect(db)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, role, content
        FROM messages
    """)

    row = cursor.fetchone()

    conn.close()

    assert row == (
        "user-1",
        "assistant",
        "Hello, how can I help you?"
    )

def test_get_recent_messages(tmp_path):
    db = tmp_path / "chat.db"

    init_database(str(db))

    memory = MemoryService(str(db))

    user = "user-1"
    
    memory.add_message(
        user,
        "user",
        "Hello"
    )

    memory.add_message(
        user,
        "assistant",
        "Hi!"
    )

    memory.add_message(
        user,
        "user",
        "How are you?"
    )

    memory.add_message(
        user,
        "assistant",
        "I'm fine."
    )

    messages = memory.get_recent_messages(
        user,
        limit=10,
    )

    assert len(messages) == 4

    assert messages[0]["role"] == "user"
    assert messages[0]["message"] == "Hello"

    assert messages[1]["role"] == "assistant"
    assert messages[1]["message"] == "Hi!"

    assert messages[2]["role"] == "user"
    assert messages[2]["message"] == "How are you?"

    assert messages[3]["role"] == "assistant"
    assert messages[3]["message"] == "I'm fine."

def test_get_recent_messages_limit(tmp_path):
    db = tmp_path / "chat.db"

    init_database(str(db))

    memory = MemoryService(str(db))

    for i in range(20):
        memory.add_message(
            "user-1",
            "user",
            f"Message {i}"
        )

    messages = memory.get_recent_messages(
        "user-1",
        limit=10
    )

    assert len(messages) == 10

    assert messages[0]["message"] == "Message 10"
    assert messages[-1]["message"] == "Message 19"

def test_empty_history(tmp_path):
    db = tmp_path / "chat.db"

    init_database(str(db))

    memory = MemoryService(str(db))

    messages = memory.get_recent_messages(
        "new-user",
        limit=10,
    )

    assert messages == []

def test_message_order(tmp_path):
    db = tmp_path / "chat.db"

    init_database(str(db))

    memory = MemoryService(str(db))

    memory.add_message("user-1", "user", "First")
    memory.add_message("user-1", "assistant", "Second")
    memory.add_message("user-1", "user", "Third")
    memory.add_message("user-1", "assistant", "Fourth")

    messages = memory.get_recent_messages(
        "user-1",
        limit=10,
    )

    assert [m["message"] for m in messages] == [
        "First",
        "Second",
        "Third",
        "Fourth",
    ]