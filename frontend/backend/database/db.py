import sqlite3
from pathlib import Path
from typing import Any


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[1]
DATABASE_PATH = BASE_DIR / "hervoice.db"


# =========================================================
# CONNECTION
# =========================================================

def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False,
    )

    connection.row_factory = sqlite3.Row

    return connection


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_db() -> None:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            mode TEXT NOT NULL,
            language TEXT NOT NULL,
            created_at TEXT NOT NULL,

            FOREIGN KEY (session_id)
                REFERENCES sessions(session_id)
        )
        """
    )

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_messages_session
        ON messages(session_id)
        """
    )

    connection.commit()
    connection.close()


# =========================================================
# SESSION
# =========================================================

def create_session(
    session_id: str,
    created_at: str,
) -> None:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO sessions (
            session_id,
            created_at
        )
        VALUES (?, ?)
        """,
        (
            session_id,
            created_at,
        ),
    )

    connection.commit()
    connection.close()


# =========================================================
# SAVE MESSAGE
# =========================================================

def save_message(
    session_id: str,
    role: str,
    content: str,
    mode: str,
    language: str,
    created_at: str,
) -> None:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO messages (
            session_id,
            role,
            content,
            mode,
            language,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            session_id,
            role,
            content,
            mode,
            language,
            created_at,
        ),
    )

    connection.commit()
    connection.close()


# =========================================================
# RECENT MESSAGES
# =========================================================

def get_recent_messages(
    session_id: str,
    limit: int = 12,
) -> list[dict[str, Any]]:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            role,
            content,
            mode,
            language,
            created_at
        FROM messages
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (
            session_id,
            limit,
        ),
    )

    rows = cursor.fetchall()

    connection.close()

    # Database gives newest first.
    # LLM needs chronological order.
    rows.reverse()

    return [
        {
            "role": row["role"],
            "content": row["content"],
            "mode": row["mode"],
            "language": row["language"],
            "created_at": row["created_at"],
        }
        for row in rows
    ]


# =========================================================
# FULL SESSION HISTORY
# =========================================================

def get_session_messages(
    session_id: str,
    limit: int = 100,
) -> list[dict[str, Any]]:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            role,
            content,
            mode,
            language,
            created_at
        FROM messages
        WHERE session_id = ?
        ORDER BY id ASC
        LIMIT ?
        """,
        (
            session_id,
            limit,
        ),
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        {
            "role": row["role"],
            "content": row["content"],
            "mode": row["mode"],
            "language": row["language"],
            "created_at": row["created_at"],
        }
        for row in rows
    ]