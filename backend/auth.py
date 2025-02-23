import firebase_admin
from firebase_admin import credentials, auth, firestore
from fastapi import HTTPException
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Firebase Admin SDK (if not already initialized)
if not firebase_admin._apps:
    cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS"))
    firebase_admin.initialize_app(cred)

# Firestore Database Instance
db = firestore.client()

# Function to verify Firebase token & retrieve role
def verify_firebase_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token["uid"]

        # Fetch user role from Firestore
        user_doc = db.collection("users").document(uid).get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            return {"uid": uid, "role": user_data.get("role", "student")}  # Default role = "student"
        else:
            raise HTTPException(status_code=404, detail="User Not Found!")

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase Token")

# Function to assign a role to a user (Admin only)
def assign_user_role(uid: str, role: str):
    try:
        db.collection("users").document(uid).set({"role": role}, merge=True)
        auth.set_custom_user_claims(uid, {"role": role})
        return {"message": f"Role '{role}' assigned to user {uid}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Function to retrieve a user’s role
def get_user_role(uid: str):
    try:
        user = auth.get_user(uid)
        return {"uid": uid, "role": user.custom_claims.get("role", "No role assigned")}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
