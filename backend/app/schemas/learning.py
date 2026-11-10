from datetime import datetime
from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class QuestionAttempt(BaseModel):
    topic: str
    difficulty: Literal["easy", "medium", "hard"]
    is_correct: bool
    confidence: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
        description="Confidence percentage (0-100) or scaled rating",
    )
    time_spent_seconds: Optional[float] = None
    question_text: Optional[str] = None
    user_answer: Optional[str] = None
    correct_answer: Optional[str] = None


class BatchQuizSubmission(BaseModel):
    session_id: str
    document_id: str
    attempts: List[QuestionAttempt]


class WeaknessPattern(BaseModel):
    pattern_type: Literal[
        "advanced_concept_struggle",
        "fundamental_inconsistency",
        "misconception_alert",
        "underconfidence",
        "retention_decay",
        "foundation_gap",
    ]
    topic: str
    severity: Literal["low", "medium", "high"]
    summary: str
    actionable_tip: str


class TopicMasteryProfile(BaseModel):
    topic: str
    mastery_score: float = Field(..., description="Weighted mastery score (0-100)")
    bkt_p_known: float = Field(..., description="Bayesian Knowledge Tracing probability of knowing (0.0-1.0)")
    confidence_score: float = Field(default=0.0, description="Average reported confidence (0-100)")
    
    total_attempts: int = 0
    correct_attempts: int = 0
    
    easy_attempts: int = 0
    easy_correct: int = 0
    easy_accuracy: float = 0.0
    
    medium_attempts: int = 0
    medium_correct: int = 0
    medium_accuracy: float = 0.0
    
    hard_attempts: int = 0
    hard_correct: int = 0
    hard_accuracy: float = 0.0
    
    consecutive_correct: int = 0
    consecutive_incorrect: int = 0
    
    last_reviewed: Optional[datetime] = None
    next_review: Optional[datetime] = None
    interval_days: int = 1
    ease_factor: float = 2.5
    is_due_for_review: bool = False
    
    learning_status: Literal["unstarted", "struggling", "developing", "mastered", "review_due"] = "unstarted"
    calibration_status: Literal["uncalibrated", "well_calibrated", "overconfident", "underconfident"] = "uncalibrated"
    detected_weaknesses: List[str] = []


class LearningRecommendation(BaseModel):
    topic: str
    recommended_activity: Literal["notes_review", "quiz_practice", "flashcard_revision", "mastery_challenge"]
    recommended_difficulty: Literal["easy", "medium", "hard"]
    reasoning: str
    pedagogical_goal: str
    urgency: Literal["critical_review", "foundation_repair", "skill_reinforcement", "progression", "enrichment"]


class LearningPathNode(BaseModel):
    topic: str
    order_index: int
    status: Literal["locked", "ready", "in_progress", "mastered", "review_due"]
    mastery_score: float
    bkt_p_known: float
    prerequisites: List[str]
    is_unlocked: bool
    recommended_next_step: str


class LearningPathResponse(BaseModel):
    session_id: str
    document_id: str
    nodes: List[LearningPathNode]
    current_focus_topic: Optional[str] = None
    completed_topics_count: int = 0
    total_topics_count: int = 0


class LearnerProfileResponse(BaseModel):
    session_id: str
    document_id: str
    overall_mastery: float
    overall_bkt: float
    overall_accuracy: float
    total_questions_attempted: int
    topic_profiles: Dict[str, TopicMasteryProfile]
    weaknesses: List[WeaknessPattern]
    due_reviews: List[str]
    primary_recommendation: Optional[LearningRecommendation] = None

