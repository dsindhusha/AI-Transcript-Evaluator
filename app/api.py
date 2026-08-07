from pathlib import Path
import shutil
import tempfile

from fastapi import (
    FastAPI,
    File,
    Form,
    UploadFile,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

    temp_path = None

    try:

        suffix = Path(file.filename).suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp:

            shutil.copyfileobj(file.file, temp)
            temp_path = Path(temp.name)

        transcript = whisper.transcribe_audio(
            temp_path
        )

        return {
            "transcript": transcript
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if temp_path and temp_path.exists():
            temp_path.unlink()


@app.post(
    "/evaluate",
    response_model=EvaluationResponse
)
def evaluate(request: EvaluationRequest):

    try:

        report = evaluator.evaluate(
            request.ground_truth,
            request.generated
        )

        score_breakdown = scoring.get_score_breakdown(
            report
        )

        report["score"] = score_breakdown["final_score"]

        report["score_breakdown"] = score_breakdown

        return report

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post(
    "/evaluate-audio",
    response_model=AudioEvaluationResponse
)
async def evaluate_audio(
    file: UploadFile = File(...),
    ground_truth: str = Form(...)
):

    temp_path = None

    try:

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

        report = evaluator.evaluate(
            ground_truth,
            generated_transcript
        )

        score_breakdown = scoring.get_score_breakdown(
            report
        )

        return {

            "generated_transcript": generated_transcript,

            "score": score_breakdown["final_score"],

            "score_breakdown": score_breakdown,

            "missing_information":
                report["missing_information"],

            "incorrect_information":
                report["incorrect_information"],

            "conflicting_information":
                report["conflicting_information"],

            "extra_information":
                report["extra_information"]

        }

    except Exception as e:

        message = str(e)

        if "RESOURCE_EXHAUSTED" in message:

            raise HTTPException(
                status_code=429,
                detail="Gemini API quota exceeded. Please try again later."
            )

        raise HTTPException(
            status_code=500,
            detail=message
        )

    finally:

        if temp_path and temp_path.exists():
            temp_path.unlink()