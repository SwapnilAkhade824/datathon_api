import firebase_admin
from firebase_admin import credentials, auth
import os

def initialize_firebase():
    if not firebase_admin._apps:
        cred_path = os.getenv("FIREBASE_CREDENTIALS", "firebase_admin.json")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

def verify_id_token(id_token):
    return auth.verify_id_token(id_token)
