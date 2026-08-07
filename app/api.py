from pathlib import Path
import shutil
import tempfile

from fastapi import FastAPI, File, Form, UploadFile

from app.models import (
    EvaluationRequest,
    EvaluationResponse,
    TranscriptionResponse,
    AudioEvaluationResponse
)

from app.services.evaluator_service import EvaluatorService
from app.services.scoring_service import ScoringService
from app.services.whisper_service import WhisperService


app = FastAPI(
    title="AI Transcript Evaluator",
    description="AI Framework for Comparing Audio and Transcript",
    version="1.0.0"
)

evaluator = EvaluatorService()
scoring = ScoringService()
whisper = WhisperService()


@app.get("/")
def home():
    return {
        "message": "AI Transcript Evaluator API is running successfully!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post(
    "/transcribe",
    response_model=TranscriptionResponse
)
async def transcribe(file: UploadFile = File(...)):

    suffix = Path(file.filename).suffix

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp:

        shutil.copyfileobj(file.file, temp)
        temp_path = Path(temp.name)

    transcript = whisper.transcribe_audio(temp_path)

    temp_path.unlink()

    return {
        "transcript": transcript
    }


@app.post(
    "/evaluate",
    response_model=EvaluationResponse
)
def evaluate(request: EvaluationRequest):

    report = evaluator.evaluate(
        request.ground_truth,
        request.generated
    )

    score = scoring.calculate_score(report)

    report["score"] = score

    return report


@app.post(
    "/evaluate-audio",
    response_model=AudioEvaluationResponse
)
async def evaluate_audio(
    file: UploadFile = File(...),
    ground_truth: str = Form(...)
):

    suffix = Path(file.filename).suffix

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp:

        shutil.copyfileobj(file.file, temp)
        temp_path = Path(temp.name)

    generated_transcript = whisper.transcribe_audio(
        temp_path
    )

    temp_path.unlink()

    report = evaluator.evaluate(
        ground_truth,
        generated_transcript
    )

    score = scoring.calculate_score(report)

    return {
        "generated_transcript": generated_transcript,
        "score": score,
        "missing_information": report["missing_information"],
        "incorrect_information": report["incorrect_information"],
        "conflicting_information": report["conflicting_information"],
        "extra_information": report["extra_information"]
    }