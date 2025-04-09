import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("firebase_admin.json")  # Path to your JSON file
firebase_admin.initialize_app(cred)
