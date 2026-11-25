
import sqlite3
from pathlib import Path

# Store the database file inside the StudySpace folder
DB_PATH = Path(__file__).resolve().parent / "studyspace.db"


def get_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create the database tables if they don't exist."""
    conn = get_connection()

    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL DEFAULT '',
                FOREIGN KEY (course_id)
                    REFERENCES courses(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                deadline TEXT NOT NULL,
                priority TEXT NOT NULL DEFAULT 'Medium',
                status TEXT NOT NULL DEFAULT 'Pending',
                FOREIGN KEY (course_id)
                    REFERENCES courses(id) ON DELETE CASCADE
            );
        """)

        conn.commit()
        print("StudySpace database initialized successfully!")

    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
