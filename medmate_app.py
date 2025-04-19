import sqlite3

def create_tables():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # User table
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT)""")

    # Reminders
    c.execute("""CREATE TABLE IF NOT EXISTS reminders (
                username TEXT, med_name TEXT, dosage TEXT, times_per_day INTEGER,
                start_date TEXT, end_date TEXT)""")

    # Appointments
    c.execute("""CREATE TABLE IF NOT EXISTS appointments (
                username TEXT, doctor TEXT, date TEXT, time TEXT, reason TEXT)""")

    # Health logs
    c.execute("""CREATE TABLE IF NOT EXISTS health_logs (
                username TEXT, temperature REAL, symptoms TEXT, mood TEXT, log_time TEXT)""")

    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = c.fetchone()
    conn.close()
    return result
def is_admin(username):
    return username == "admin"

