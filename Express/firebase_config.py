import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
firestore_client = firestore.client()