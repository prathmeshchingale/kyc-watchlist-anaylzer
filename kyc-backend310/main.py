from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\pchingale\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
import face_recognition
import cv2
import shutil
import os
from PIL import Image
from fuzzywuzzy import fuzz
from uuid import uuid4
import numpy as np

# ---------- Config ----------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] for all origins (not recommended for prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

client = MongoClient("mongodb://localhost:27017")
db = client["kyc"]
collection = db["submissions"]

# ---------- Utility Functions ----------
def save_file(upload_file: UploadFile, prefix: str):
    file_path = os.path.join(UPLOAD_DIR, f"{prefix}_{upload_file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path

def extract_text(img_path):
    try:
        img = Image.open(img_path)
        return pytesseract.image_to_string(img)
    except Exception:
        return ""

def extract_face(image_path):
    try:
        # Open image using PIL and convert to RGB
        pil_image = Image.open(image_path).convert("RGB")
        img = np.array(pil_image)

        # Ensure it’s 8-bit RGB
        if img.dtype != np.uint8:
            img = img.astype(np.uint8)

        encodings = face_recognition.face_encodings(img)
        return encodings[0] if encodings else None
    except Exception as e:
        print(f"Face extraction failed for {image_path}: {e}")
        return None


def fuzzy_match(a, b):
    return fuzz.token_sort_ratio(a.lower(), b.lower())

# ---------- WorldCheck Dummy List ----------
worldcheck = [
    {"name": "RAHUL SHARMA", "location": "DELHI"},
    {"name": "PRIYA MEHRA", "location": "MUMBAI"},
    {"name": "SUNIL JADHAV", "location": "PUNE"},
]

# ---------- API Endpoint ----------
@app.post("/upload")
def upload(
    user_id: str = Form(...),
    document_type: str = Form(...),
    consent_given: bool = Form(...),
    front_file: UploadFile = File(...),
    back_file: UploadFile = File(...),
    selfie_file: UploadFile = File(...),
):
    if not consent_given:
        raise HTTPException(status_code=400, detail="Consent is required.")

    submission_id = str(uuid4())
    front_path = save_file(front_file, f"{submission_id}_front")
    back_path = save_file(back_file, f"{submission_id}_back")
    selfie_path = save_file(selfie_file, f"{submission_id}_selfie")

    # OCR
    front_text = extract_text(front_path)
    back_text = extract_text(back_path)
    extracted_text = front_text + "\n" + back_text

    # Extract fields
    name = ""
    address = ""
    for line in extracted_text.split("\n"):
        if len(line.split()) >= 2 and not name:
            name = line.strip()
        if any(p in line.lower() for p in ["india", "road", "nagar", "pincode", "street"]):
            address += line.strip() + " "

    # Face comparison
    doc_face = extract_face(front_path)
    selfie_face = extract_face(selfie_path)
    face_match = False
    if doc_face is not None and selfie_face is not None:
        face_match = face_recognition.compare_faces([doc_face], selfie_face)[0]

    # WorldCheck match
    fraud_flag = False
    risk_score = 0
    for entry in worldcheck:
        if fuzzy_match(entry["name"], name) > 85 and fuzzy_match(entry["location"], address) > 70:
            fraud_flag = True
            risk_score = 90
            break

    record = {
        "submission_id": submission_id,
        "user_id": user_id,
        "document_type": document_type,
        "consent": consent_given,
        "name": name,
        "address": address.strip(),
        "face_match": face_match,
        "fraud_flag": fraud_flag,
        "risk_score": risk_score,
    }

    collection.insert_one(record)

    return {"id": submission_id, "face_match": face_match, "fraud_flag": fraud_flag, "risk_score": risk_score}
