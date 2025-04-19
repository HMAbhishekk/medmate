from database import get_connection

def save_reminder(username, med_name, dosage, times, start, end):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO reminders VALUES (?, ?, ?, ?, ?, ?)", (username, med_name, dosage, times, start, end))
    conn.commit()
    conn.close()

def get_todays_reminders(username, today):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT med_name FROM reminders WHERE username=? AND start_date<=? AND end_date>=?", (username, today, today))
    results = c.fetchall()
    conn.close()
    return [{"med_name": r[0]} for r in results]

def save_appointment(username, doctor, date, time, reason):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO appointments VALUES (?, ?, ?, ?, ?)", (username, doctor, date, time, reason))
    conn.commit()
    conn.close()

def get_todays_appointments(username, today):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT doctor FROM appointments WHERE username=? AND date=?", (username, today))
    results = c.fetchall()
    conn.close()
    return [{"doctor": r[0]} for r in results]

def save_health_log(username, temp, symptoms, mood, timestamp):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?)", (username, temp, symptoms, mood, timestamp))
    conn.commit()
    conn.close()
