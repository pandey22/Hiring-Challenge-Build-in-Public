from fastapi import FastAPI, Depends, HTTPException
import firebase_admin
from firebase_admin import credentials, auth, firestore
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Enable CORS for Vue.js frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5175,https://hiring-challenge-build-in-public.onrender.com"],  # Update this if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase Admin SDK
SERVICE_ACCOUNT_PATH = os.getenv("FIREBASE_CREDENTIALS")  # Get from .env
if not firebase_admin._apps:  # Prevent re-initialization
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)

# Firestore Database Instance
db = firestore.client()

# Request Model
class TokenData(BaseModel):
    token: str  # Firebase ID token sent from frontend

# Verify Firebase ID Token
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

# Route - Verify Firebase Authentication & Return Role
@app.post("/verify")
async def verify_user(data: TokenData):
    return verify_firebase_token(data.token)

# Route - Assign Role to User (Admin Only)
@app.post("/assign-role/{uid}/{role}")
async def assign_role(uid: str, role: str):
    try:
        # Update role in Firestore
        db.collection("users").document(uid).set({"role": role}, merge=True)
        # Assign role in Firebase Custom Claims
        auth.set_custom_user_claims(uid, {"role": role})
        return {"message": f"Role '{role}' assigned to user {uid}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Route - Fetch User Role
@app.get("/get-role/{uid}")
async def get_role(uid: str):
    user = auth.get_user(uid)
    role = user.custom_claims.get("role", "No role assigned")
    return {"uid": uid, "role": role}

@app.get("/")
async def root():
    return {"message": "FastAPI Backend is Running"}
