# firebase_users.py
from firebase_config import db

def add_user(username, password):
    db.collection("users").document(username).set({
        "password": password
    })

def login_user(username, password):
    doc_ref = db.collection("users").document(username).get()
    if doc_ref.exists and doc_ref.to_dict().get("password") == password:
        return True
    return False

def is_admin(username):
    return username == "admin"
