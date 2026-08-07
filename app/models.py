from pydantic import BaseModel


class EvaluationRequest(BaseModel):
    ground_truth: str
    generated: str


class EvaluationResponse(BaseModel):
    score: int
    missing_information: list
    incorrect_information: list
    conflicting_information: list
    extra_information: list


class TranscriptionResponse(BaseModel):
    transcript: str


class AudioEvaluationResponse(BaseModel):
    generated_transcript: str
    score: int
    missing_information: list
    incorrect_information: list
    conflicting_information: list
    extra_information: list