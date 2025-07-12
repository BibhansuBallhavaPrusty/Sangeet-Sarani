import sqlite3

conn = sqlite3.connect('database/students.db')
c = conn.cursor()

# Table for student registrations
c.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        course TEXT,
        level TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Table for contact messages
c.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()
print("✅ Database initialized.")