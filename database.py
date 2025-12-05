import sqlite3

DB_NAME = "lexy.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        # Notes
        c.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Reminders
        c.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT,
                remind_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Schedule
        c.execute('''
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event TEXT,
                event_date TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

# ----- Notes -----
def add_note(content: str):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO notes (content) VALUES (?)", (content,))
        conn.commit()

def get_notes():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT id, content, created_at FROM notes ORDER BY created_at DESC")
        return c.fetchall()

def delete_note(note_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()

def delete_all_notes():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM notes")
        conn.commit()

# ----- Schedule -----
def add_schedule(event: str, event_date: str):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO schedule (event, event_date) VALUES (?, ?)", (event, event_date))
        conn.commit()

def get_schedule():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT id, event, event_date FROM schedule ORDER BY event_date ASC")
        return c.fetchall()

def delete_schedule(sched_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM schedule WHERE id = ?", (sched_id,))
        conn.commit()

def delete_all_schedule():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM schedule")
        conn.commit()

# ----- Reminders -----
def add_reminder(content: str, remind_at: str):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO reminders (content, remind_at) VALUES (?, ?)", (content, remind_at))
        conn.commit()

def get_reminders():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT id, content, remind_at FROM reminders ORDER BY remind_at ASC")
        return c.fetchall()

def delete_reminder(rem_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM reminders WHERE id = ?", (rem_id,))
        conn.commit()

def delete_all_reminders():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM reminders")
        conn.commit()
