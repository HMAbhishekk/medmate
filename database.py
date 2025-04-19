import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect("medmate.db")
    c = conn.cursor()

    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )''')

    # Medication reminders
    c.execute('''CREATE TABLE IF NOT EXISTS reminders (
        username TEXT, med_name TEXT, dosage TEXT, times INTEGER,
        start_date TEXT, end_date TEXT
    )''')

    # Appointments
    c.execute('''CREATE TABLE IF NOT EXISTS appointments (
        username TEXT, doctor TEXT, date TEXT, time TEXT, reason TEXT
    )''')

    # Health logs
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
        username TEXT, temperature REAL, symptoms TEXT, mood TEXT, timestamp TEXT
    )''')

    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect("medmate.db")
