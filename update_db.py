import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE users ADD COLUMN resume_uploaded INTEGER DEFAULT 0")
except:
    pass

try:
    cursor.execute("ALTER TABLE users ADD COLUMN resume_filename TEXT")
except:
    pass

try:
    cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT")
except:
    pass

try:
    cursor.execute("ALTER TABLE users ADD COLUMN skills TEXT")
except:
    pass

try:
    cursor.execute("ALTER TABLE users ADD COLUMN average_score INTEGER DEFAULT 0")
except:
    pass

try:
    cursor.execute(
        "ALTER TABLE users ADD COLUMN interviews_completed INTEGER DEFAULT 0"
    )
except:
    pass

conn.commit()
conn.close()

print("Database Updated Successfully ")
