```markdown

# 🛡️ kyc-watchlist-anaylzer

An AI-powered KYC (Know Your Customer) verification tool that allows users to upload government-issued identity documents and selfies for automated face matching, document parsing, and fraud risk scoring.

---

## 🚀 Features

- Upload Aadhaar or PAN images (front + back) and a selfie
- Face matching using `face_recognition`
- Text extraction from ID cards using OCR
- Risk score and fraud flag generation
- Consent-based data handling
- Stores metadata and result in MongoDB
- Designed for easy deployment and integration

---

## 🧠 Tech Stack

| Layer      | Technology Used                      |
|------------|---------------------------------------|
| Frontend   | React.js (Vite)                       |
| Backend    | FastAPI (Python 3.10+)                |
| OCR        | `pytesseract`                         |
| Face Match | `face_recognition`, `dlib`, `opencv` |
| Storage    | MongoDB                               |

---

## 📂 Project Structure

```

kyc-fraud-detector/
│
├── frontend/             # React-based UI
├── backend/              # FastAPI-based server
│   ├── main.py           # API endpoints
│   ├── utils/            # Helper scripts (OCR, face match)
│   └── uploads/          # Uploaded images
├── README.md             # You're here!
└── requirements.txt      # Backend Python dependencies

````

---

## ⚙️ Setup Instructions

### 🔧 Backend Setup (Python 3.10+)

1. Clone the repo and navigate:
   ```bash
   git clone https://github.com/your-username/kyc-fraud-detector.git
   cd kyc-fraud-detector/backend
````

2. Create a virtual environment (Python 3.10 recommended):
	
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate     # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the backend server:

   ```bash
   uvicorn main:app --reload
   ```

> Make sure MongoDB is running locally (default port: 27017). Update the connection URI in `main.py` if needed.

---

### 🌐 Frontend Setup

1. Navigate to the frontend folder:

   ```bash
   cd ../frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm run dev
   ```

> The frontend runs on [http://localhost:3000](http://localhost:3000) and communicates with the backend at [http://localhost:8000](http://localhost:8000)

---

## 🧪 Sample Flow

1. Upload:

   * Aadhaar front image
   * Aadhaar back image
   * Selfie image

2. Review auto-extracted details and give consent

3. Backend performs:

   * Text extraction from Aadhaar using OCR
   * Face matching with selfie
   * Risk scoring

4. Results saved in MongoDB:

   * `submission_id`, `user_id`, `face_match`, `fraud_flag`, `risk_score`, etc.

---

## 📝 API Endpoints (FastAPI)

| Method | Endpoint  | Description            |
| ------ | --------- | ---------------------- |
| POST   | `/upload` | Uploads 3 images       |
| POST   | `/submit` | Submits extracted data |
| GET    | `/ping`   | Health check           |

---

## 🛡️ Notes

* Only JPEG and PNG images are supported.
* Avoid uploading PDFs or scanned PDFs.
* Face recognition requires RGB or grayscale 8-bit images.

---

## 🤝 Contribution

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is under the [MIT License](LICENSE).

---
