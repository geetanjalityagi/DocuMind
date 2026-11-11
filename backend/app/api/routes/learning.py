from fastapi import APIRouter, HTTPException
from typing import List, Optional

from app.schemas.learning import (
    BatchQuizSubmission,
    LearnerProfileResponse,
    LearningPathResponse,
    LearningRecommendation,
    QuestionAttempt,
)
from app.services.learning_service import (
    get_adaptive_learning_path,
    get_learner_profile,
    record_batch_quiz_submission,
    record_question_attempt,
)
from app.services.topic_service import extract_topics

router = APIRouter(
    prefix="/learning",
    tags=["Adaptive Learning Engine"],
)


@router.post("/attempt")
async def log_attempt(session_id: str, document_id: str, attempt: QuestionAttempt):
    """
    Records an individual student answer attempt and immediately updates:
    - Bayesian Knowledge Tracing (BKT) probability
    - Weighted mastery score
    - Spaced repetition (SM-2) schedule
    - Confidence calibration check
    """
    try:
        updated_topic = record_question_attempt(session_id, document_id, attempt)
        return {
            "status": "success",
            "topic": updated_topic["topic"],
            "mastery_score": updated_topic["mastery_score"],
            "bkt_p_known": updated_topic["bkt_p_known"],
            "learning_status": updated_topic["learning_status"],
            "calibration_status": updated_topic["calibration_status"],
            "next_review": updated_topic["next_review"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record attempt: {e}")


@router.post("/submit-quiz", response_model=LearnerProfileResponse)
async def submit_quiz(submission: BatchQuizSubmission):
    """
    Batch logs all question attempts from a completed quiz assessment,
    running weakness detection and recomputing the global learner profile.
    """
    try:
        profile = record_batch_quiz_submission(submission)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit quiz batch: {e}")


@router.get("/profile/{session_id}/{document_id}", response_model=LearnerProfileResponse)
async def get_profile(session_id: str, document_id: str):
    """
    Retrieves the rich multidimensional learner model:
    - BKT knowledge acquisition probability
    - Difficulty-level breakdown (easy, medium, hard accuracy)
    - Weakness & error pattern analysis (Student A vs Student B detection)
    - Overconfidence / underconfidence calibration
    - Overdue spaced repetition items
    """
    try:
        return get_learner_profile(session_id, document_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch profile: {e}")


@router.get("/recommendation/{session_id}/{document_id}", response_model=Optional[LearningRecommendation])
async def get_recommendation(session_id: str, document_id: str):
    """
    Returns the next optimal learning activity with transparent explanation
    of why it was chosen based on the student's mastery and error patterns.
    """
    try:
        profile = get_learner_profile(session_id, document_id)
        return profile.primary_recommendation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch recommendation: {e}")


@router.get("/path/{session_id}/{document_id}", response_model=LearningPathResponse)
async def get_learning_path(session_id: str, document_id: str):
    """
    Returns an adaptive prerequisite roadmap of topics for the document,
    gating concepts based on prerequisite mastery thresholds.
    """
    try:
        available_topics: List[str] = []
        try:
            raw_topics = extract_topics(document_id)
            if isinstance(raw_topics, list):
                available_topics = [
                    t.get("name", t) if isinstance(t, dict) else str(t)
                    for t in raw_topics
                ]
        except Exception:
            pass

        return get_adaptive_learning_path(session_id, document_id, available_topics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to build learning path: {e}")

