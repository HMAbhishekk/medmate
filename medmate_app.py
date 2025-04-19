import streamlit as st
from datetime import datetime, timedelta
from sqlite_users import add_user, login_user
from sqlite_health import (
    save_reminder, get_todays_reminders,
    save_appointment, get_todays_appointments,
    save_health_log
)
from database import init_db

# Initialize database
init_db()

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
            if login_user(username, password):
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
                st.error("Username may already exist!")

# Dashboard
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
            save_reminder(username, med_name, dosage, times, start.isoformat(), end.isoformat())
            st.success("Reminder Saved!")

    elif menu == "📅 Appointments":
        st.subheader("Book Appointment")
        doc = st.text_input("Doctor")
        date = st.date_input("Date")
        time = st.time_input("Time")
        reason = st.text_area("Reason")

        if st.button("Book"):
            save_appointment(username, doc, date.isoformat(), time.strftime("%H:%M"), reason)
            st.success("Appointment Booked!")

    elif menu == "📊 Logs":
        st.subheader("Log Health Info")
        temp = st.number_input("Temperature (°C)", 35.0, 42.0)
        symptoms = st.text_area("Symptoms")
        mood = st.selectbox("Mood", ["😄 Good", "😐 Okay", "😔 Bad"])
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        if st.button("Save Log"):
            save_health_log(username, temp, symptoms, mood, now)
            st.success("Health Log Saved!")

    elif menu == "🚪 Logout":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# Show Today's Reminders/Notifications
def show_notifications(username):
    today = datetime.today().date().isoformat()
    meds_today = get_todays_reminders(username, today)
    if meds_today:
        st.info("💡 You have medication reminders today: " + ", ".join(m['med_name'] for m in meds_today))

    apps_today = get_todays_appointments(username, today)
    for appt in apps_today:
        st.warning(f"📅 You have an appointment with Dr. {appt['doctor']} today!")

# App Launch
if not st.session_state.logged_in:
    login_register()
else:
    dashboard(st.session_state.username)
