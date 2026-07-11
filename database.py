import sqlite3


def create_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        resume_uploaded INTEGER DEFAULT 0,
        resume_filename TEXT,
        phone TEXT,
        skills TEXT,
        average_score INTEGER DEFAULT 0,
        interviews_completed INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()



