import streamlit as st
from datetime import datetime, timedelta
import sqlite3
from database import create_tables, add_user, login_user

# Setup
create_tables()
st.set_page_config(page_title="MedMate", page_icon="💊", layout="centered")

# Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Login/Register Page
def login_register():
    st.title("💊 MedMate Login")
    menu = st.radio("Choose Option", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if menu == "Login":
        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.success(f"Welcome back, {username}!")
                st.session_state.logged_in = True
                st.session_state.username = username
            else:
                st.error("Invalid username or password")
    else:
        if st.button("Register"):
            try:
                add_user(username, password)
                st.success("Account created! You can log in now.")
            except:
                st.error("Username already exists!")

# Logged-in Dashboard
def dashboard(username):
    st.sidebar.success(f"Logged in as {username}")
    menu = st.sidebar.radio("Navigate", ["🏠 Home", "💉 Medication", "📅 Appointments", "📊 Logs", "🚪 Logout"])

    if menu == "🏠 Home":
        st.title("💊 MedMate Dashboard")
        st.write("Welcome to your health dashboard!")
        show_notifications(username)

    elif menu == "💉 Medication":
        st.subheader("Set a Medication Reminder")
        med_name = st.text_input("Medicine Name")
        dosage = st.text_input("Dosage")
        times = st.slider("Times per Day", 1, 4)
        start = st.date_input("Start Date", datetime.today())
        end = st.date_input("End Date", datetime.today() + timedelta(days=7))

        if st.button("Save Reminder"):
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            c.execute("INSERT INTO reminders VALUES (?, ?, ?, ?, ?, ?)",
                      (username, med_name, dosage, times, start.isoformat(), end.isoformat()))
            conn.commit()
            conn.close()
            st.success("Reminder Saved!")

    elif menu == "📅 Appointments":
        st.subheader("Book Appointment")
        doc = st.text_input("Doctor")
        date = st.date_input("Date")
        time = st.time_input("Time")
        reason = st.text_area("Reason")

        if st.button("Book"):
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            c.execute("INSERT INTO appointments VALUES (?, ?, ?, ?, ?)",
                      (username, doc, date.isoformat(), time.strftime("%H:%M"), reason))
            conn.commit()
            conn.close()
            st.success("Appointment Booked!")

    elif menu == "📊 Logs":
        st.subheader("Log Health Info")
        temp = st.number_input("Temperature (°C)", 35.0, 42.0)
        symptoms = st.text_area("Symptoms")
        mood = st.selectbox("Mood", ["😄 Good", "😐 Okay", "😔 Bad"])
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        if st.button("Save Log"):
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            c.execute("INSERT INTO health_logs VALUES (?, ?, ?, ?, ?)",
                      (username, temp, symptoms, mood, now))
            conn.commit()
            conn.close()
            st.success("Health Log Saved!")

    elif menu == "🚪 Logout":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# Simple Notification System
def show_notifications(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    today = datetime.today().date().isoformat()
    c.execute("SELECT med_name FROM reminders WHERE username = ? AND start_date <= ? AND end_date >= ?", (username, today, today))
    meds_today = c.fetchall()
    if meds_today:
        st.info(f"💡 You have medication reminders today: " + ", ".join(m[0] for m in meds_today))
    c.execute("SELECT date, doctor FROM appointments WHERE username = ? AND date = ?", (username, today))
    apps = c.fetchall()
    if apps:
        st.warning(f"📅 You have an appointment with Dr. {apps[0][1]} today!")
    conn.close()

# App Launch
if not st.session_state.logged_in:
    login_register()
else:
    dashboard(st.session_state.username)
