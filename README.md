# AI Transcript Evaluator

Evaluate speech transcripts using **Faster Whisper** and **Google Gemini AI**. Upload an audio file along with its corresponding ground truth transcript to generate an evaluation report containing an overall score, score breakdown, and detailed error analysis.

---

## Requirements

- Python 3.10 or later
- pip
- Google Gemini API Key

---

## Clone Repository

```bash
git clone https://github.com/dsindhusha/AI-Transcript-Evaluator.git

cd AI-Transcript-Evaluator
```

---

## Create a Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

You can generate a Gemini API key from:

https://aistudio.google.com/

---

## Run the Backend

Start the FastAPI server.

```bash
uvicorn app.api:app --reload
```

Backend URL:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

---

## Run the Frontend

Open another terminal.

```bash
cd frontend

python -m http.server 5500
```

Open the application in your browser.

```
http://localhost:5500
```

---

## Quick Test

1. Start the backend.
2. Start the frontend.
3. Open `http://localhost:5500`.
4. Upload an audio file.
5. Paste the corresponding ground truth transcript.
6. Click **Evaluate Audio**.
7. View the generated transcript, overall score, score breakdown, and evaluation results.

---

## Project Structure

```text
AI-Transcript-Evaluator/
│
├── app/
│   ├── services/
│   ├── api.py
│   ├── main.py
│   ├── models.py
│   ├── prompts.py
│   └── score_reports.py
│
├── dataset/
│   ├── audio/
│   ├── generated/
│   ├── ground_truth/
│   └── reports/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## API Endpoints

| Method | Endpoint | Description |
| :----- | :------- | :---------- |
| GET | `/` | Check API status |
| GET | `/health` | Health check |
| POST | `/transcribe` | Generate transcript from an uploaded audio file |
| POST | `/evaluate` | Compare two transcripts |
| POST | `/evaluate-audio` | Complete audio evaluation pipeline |

---

## Author

**Sindhusha Devarakonda**

GitHub: https://github.com/dsindhusha