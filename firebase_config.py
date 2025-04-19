import firebase_admin
from firebase_admin import credentials, firestore

# Load your Firebase service account key
cred = credentials.Certificate("serviceAccountKey.json")

# Initialize app if not already
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Get the Firestore client
db = firestore.client()
