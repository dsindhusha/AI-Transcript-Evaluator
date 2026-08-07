from pydantic import BaseModel


class EvaluationRequest(BaseModel):
    ground_truth: str
    generated: str


class ScoreCategory(BaseModel):
    count: int
    penalty: int
    deduction: int


class ScoreBreakdown(BaseModel):
    starting_score: int
    missing: ScoreCategory
    incorrect: ScoreCategory
    conflicting: ScoreCategory
    extra: ScoreCategory
    final_score: int


class EvaluationResponse(BaseModel):
    score: int
    score_breakdown: ScoreBreakdown
    missing_information: list
    incorrect_information: list
    conflicting_information: list
    extra_information: list


class TranscriptionResponse(BaseModel):
    transcript: str


class AudioEvaluationResponse(BaseModel):
    generated_transcript: str
    score: int
    score_breakdown: ScoreBreakdown
    missing_information: list
    incorrect_information: list
    conflicting_information: list
    extra_information: list