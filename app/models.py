from pydantic import BaseModel


class EvaluationRequest(BaseModel):
    """
    Request model for transcript evaluation.
    """

    ground_truth: str
    generated: str


class ScoreCategory(BaseModel):
    """
    Represents the scoring details for an evaluation category.
    """

    count: int
    penalty: int
    deduction: int


class ScoreBreakdown(BaseModel):
    """
    Represents the complete score breakdown for an evaluation.
    """

    starting_score: int
    missing: ScoreCategory
    incorrect: ScoreCategory
    conflicting: ScoreCategory
    extra: ScoreCategory
    final_score: int


class EvaluationResponse(BaseModel):
    """
    Response model for transcript evaluation results.
    """

    score: int
    score_breakdown: ScoreBreakdown
    missing_information: list
    incorrect_information: list
    conflicting_information: list
    extra_information: list


class TranscriptionResponse(BaseModel):
    """
    Response model for audio transcription.
    """

    transcript: str


class AudioEvaluationResponse(BaseModel):
    """
    Response model for complete audio evaluation results.
    """

    generated_transcript: str
    score: int
    score_breakdown: ScoreBreakdown
    missing_information: list
    incorrect_information: list
    conflicting_information: list
    extra_information: list