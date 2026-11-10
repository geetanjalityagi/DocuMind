import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from app.config import PROFILES_DIR
from app.schemas.learning import (
    BatchQuizSubmission,
    LearnerProfileResponse,
    LearningPathNode,
    LearningPathResponse,
    LearningRecommendation,
    QuestionAttempt,
    TopicMasteryProfile,
    WeaknessPattern,
)


# ─── BKT CONFIGURATION CONSTANTS ──────────────────────────────────────────────
DEFAULT_BKT_P_INIT = 0.20     # Prior probability of knowing the concept
DEFAULT_BKT_P_TRANSIT = 0.15  # Probability of learning concept on opportunity
DEFAULT_BKT_P_SLIP = 0.10     # Probability of making mistake despite knowing
DEFAULT_BKT_P_GUESS = 0.25    # Probability of guessing correctly (4-choice MCQ)


def _get_profile_path(session_id: str, document_id: str) -> Path:
    """Safe filename for storing learner profile per session and document."""
    safe_session = "".join(c for c in session_id if c.isalnum() or c in ("-", "_"))
    safe_doc = "".join(c for c in document_id if c.isalnum() or c in ("-", "_"))
    return PROFILES_DIR / f"{safe_session}_{safe_doc}.json"


def load_raw_profile(session_id: str, document_id: str) -> dict:
    """Load learner profile JSON from disk or initialize empty structure."""
    path = _get_profile_path(session_id, document_id)
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    return {
        "session_id": session_id,
        "document_id": document_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "total_questions_attempted": 0,
        "topics": {},
    }


def save_raw_profile(session_id: str, document_id: str, data: dict) -> None:
    """Persist learner profile JSON to disk."""
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    path = _get_profile_path(session_id, document_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)


# ─── BAYESIAN KNOWLEDGE TRACING (BKT) ─────────────────────────────────────────

def calculate_bkt_update(
    p_known: float,
    is_correct: bool,
    difficulty: str = "medium",
) -> float:
    """
    Standard Bayesian Knowledge Tracing (Corbett & Anderson) with
    difficulty-sensitive slip and guess parameters.
    
    Update equations:
      P(L_t | obs=Correct)   = [P(L) * (1 - P(S))] / [P(L) * (1 - P(S)) + (1 - P(L)) * P(G)]
      P(L_t | obs=Incorrect) = [P(L) * P(S)]       / [P(L) * P(S)       + (1 - P(L)) * (1 - P(G))]
      P(L_{t+1})             = P(L_t | obs) + (1 - P(L_t | obs)) * P(T)
    """
    # Difficulty adjustments for Guess and Slip
    diff = difficulty.lower()
    if diff == "easy":
        p_guess = 0.30
        p_slip = 0.08
    elif diff == "hard":
        p_guess = 0.15
        p_slip = 0.15
    else:  # medium
        p_guess = DEFAULT_BKT_P_GUESS
        p_slip = DEFAULT_BKT_P_SLIP

    p_transit = DEFAULT_BKT_P_TRANSIT

    # Ensure prior is within reasonable bounds
    p_curr = max(0.01, min(0.99, p_known))

    # 1. Posterior calculation based on evidence
    if is_correct:
        numerator = p_curr * (1.0 - p_slip)
        denominator = numerator + ((1.0 - p_curr) * p_guess)
    else:
        numerator = p_curr * p_slip
        denominator = numerator + ((1.0 - p_curr) * (1.0 - p_guess))

    p_posterior = numerator / max(1e-9, denominator)

    # 2. Knowledge acquisition transition step for next opportunity
    p_next = p_posterior + ((1.0 - p_posterior) * p_transit)

    return round(float(max(0.01, min(0.99, p_next))), 4)


# ─── WEIGHTED MASTERY ENGINE ──────────────────────────────────────────────────

def compute_weighted_mastery(topic_data: dict) -> Tuple[float, str]:
    """
    Computes a transparent, weighted mastery score (0-100) taking into account:
      - Difficulty weights: Easy=1.0, Medium=1.5, Hard=2.0
      - Volume smoothing: Laplace pseudo-trials prevent instant 100% on 1 attempt
      - Streak multipliers: bonuses for consecutive correct, penalties for consecutive wrong
      - BKT latent knowledge estimate (blended at 35% weight)
    """
    easy_att = topic_data.get("easy_attempts", 0)
    easy_cor = topic_data.get("easy_correct", 0)
    med_att = topic_data.get("medium_attempts", 0)
    med_cor = topic_data.get("medium_correct", 0)
    hard_att = topic_data.get("hard_attempts", 0)
    hard_cor = topic_data.get("hard_correct", 0)
    
    total_att = easy_att + med_att + hard_att
    if total_att == 0:
        return 0.0, "unstarted"

    # Difficulty weights
    w_easy, w_med, w_hard = 1.0, 1.5, 2.0
    weighted_correct = (easy_cor * w_easy) + (med_cor * w_med) + (hard_cor * w_hard)
    weighted_total = (easy_att * w_easy) + (med_att * w_med) + (hard_att * w_hard)

    # Bayesian volume dampener (equivalent to 4 neutral prior attempts at 50%)
    prior_weight = 4.0 * 1.25  # ~5.0
    prior_correct = prior_weight * 0.40
    smoothed_accuracy = (weighted_correct + prior_correct) / (weighted_total + prior_weight)

    # Streak modifier
    consec_c = topic_data.get("consecutive_correct", 0)
    consec_inc = topic_data.get("consecutive_incorrect", 0)
    streak_bonus = min(0.10, consec_c * 0.025)
    streak_penalty = min(0.15, consec_inc * 0.035)

    adjusted_acc = max(0.0, min(1.0, smoothed_accuracy + streak_bonus - streak_penalty))

    # Blend with BKT p_known
    bkt = topic_data.get("bkt_p_known", DEFAULT_BKT_P_INIT)
    composite_score = (adjusted_acc * 0.65) + (bkt * 0.35)
    final_mastery = round(float(composite_score * 100.0), 1)

    # Determine status
    if final_mastery >= 80.0:
        status = "mastered"
    elif final_mastery >= 50.0:
        status = "developing"
    elif total_att >= 3 and final_mastery < 45.0:
        status = "struggling"
    else:
        status = "developing"

    return final_mastery, status


# ─── SPACED REPETITION ENGINE (SM-2 ADAPTATION) ────────────────────────────────

def update_spaced_repetition(
    topic_data: dict,
    is_correct: bool,
    confidence: Optional[float] = None,
) -> Tuple[int, float, datetime, bool]:
    """
    SuperMemo-2 (SM-2) algorithm adapted for topic revision intervals.
    Generates quality score q (0-5) based on correctness and confidence:
      q=5: Perfect, confident recall
      q=4: Correct with normal confidence
      q=3: Correct with low confidence / hesitation
      q=2: Incorrect but had some idea
      q=1: Incorrect with wrong guess
      q=0: Complete lack of understanding
    """
    conf = confidence if confidence is not None else 60.0

    if is_correct:
        if conf >= 75:
            q = 5
        elif conf >= 50:
            q = 4
        else:
            q = 3
    else:
        if conf >= 75:
            q = 1  # Overconfident mistake = high disruption to retention
        elif conf >= 40:
            q = 2
        else:
            q = 2

    ease_factor = topic_data.get("ease_factor", 2.5)
    interval = topic_data.get("interval_days", 1)
    reps = topic_data.get("repetitions", 0)

    # SM-2 ease factor update formula
    # EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    ease_factor = ease_factor + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    ease_factor = max(1.3, min(3.0, round(ease_factor, 2)))

    if q < 3:
        reps = 0
        interval = 1
    else:
        if reps == 0:
            interval = 1
        elif reps == 1:
            interval = 3
        else:
            interval = max(1, int(round(interval * ease_factor)))
        reps += 1

    now = datetime.now(timezone.utc)
    next_review = now + timedelta(days=interval)

    topic_data["repetitions"] = reps
    topic_data["interval_days"] = interval
    topic_data["ease_factor"] = ease_factor
    topic_data["last_reviewed"] = now.isoformat()
    topic_data["next_review"] = next_review.isoformat()

    return interval, ease_factor, next_review, False


# ─── WEAKNESS & ERROR PATTERN DETECTOR ────────────────────────────────────────

def analyze_topic_weaknesses(topic_name: str, data: dict) -> List[WeaknessPattern]:
    """
    Pinpoints cognitive and error patterns, such as the critical distinction
    between Student A (solid basics, struggles with hard) and
    Student B (passes hard, fails basic questions).
    """
    weaknesses: List[WeaknessPattern] = []

    easy_att = data.get("easy_attempts", 0)
    easy_cor = data.get("easy_correct", 0)
    easy_acc = (easy_cor / easy_att * 100.0) if easy_att > 0 else 0.0

    med_att = data.get("medium_attempts", 0)
    med_cor = data.get("medium_correct", 0)
    med_acc = (med_cor / med_att * 100.0) if med_att > 0 else 0.0

    hard_att = data.get("hard_attempts", 0)
    hard_cor = data.get("hard_correct", 0)
    hard_acc = (hard_cor / hard_att * 100.0) if hard_att > 0 else 0.0

    total_att = data.get("total_attempts", 0)
    overconf_count = data.get("overconfident_errors", 0)
    underconf_count = data.get("underconfident_successes", 0)

    # 1. Student A Profile: Advanced Concept Struggle
    # Easy is strong (>= 75%), but Hard is struggling (< 40%)
    if easy_att >= 2 and easy_acc >= 75.0 and hard_att >= 1 and hard_acc < 40.0:
        weaknesses.append(
            WeaknessPattern(
                pattern_type="advanced_concept_struggle",
                topic=topic_name,
                severity="medium",
                summary=f"Strong on foundational questions ({easy_acc:.0f}%) but struggles on complex/hard questions ({hard_acc:.0f}%).",
                actionable_tip="Focus on multi-step synthesis and edge cases. Review study notes on complex relationships before tackling hard quizzes.",
            )
        )

    # 2. Student B Profile: Fundamental Inconsistency / Careless Flaws
    # Gets hard questions correct (>= 50%) but fails basic/easy questions (< 60%)
    if hard_att >= 1 and hard_acc >= 50.0 and easy_att >= 2 and easy_acc < 60.0:
        weaknesses.append(
            WeaknessPattern(
                pattern_type="fundamental_inconsistency",
                topic=topic_name,
                severity="high",
                summary=f"Able to solve hard questions ({hard_acc:.0f}%) yet misses basic definitions ({easy_acc:.0f}%).",
                actionable_tip="Critical gap detected: review elementary definitions and terminology. Do not advance to hard challenges until fundamentals stabilize.",
            )
        )

    # 3. Misconception Alert (High confidence + Wrong answer)
    if overconf_count >= 2:
        weaknesses.append(
            WeaknessPattern(
                pattern_type="misconception_alert",
                topic=topic_name,
                severity="high",
                summary="Repeatedly reports high confidence on incorrect answers, indicating an active misconception.",
                actionable_tip="Read the contrastive explanations and review flashcards specifically addressing common misconceptions for this topic.",
            )
        )

    # 4. Underconfidence / Imposter Phenomenon
    if underconf_count >= 3 and data.get("mastery_score", 0) >= 65.0:
        weaknesses.append(
            WeaknessPattern(
                pattern_type="underconfidence",
                topic=topic_name,
                severity="low",
                summary="Consistently answers accurately but reports low confidence scores.",
                actionable_tip="Your grasp is stronger than you perceive. Trust your intuition and attempt timed self-assessments.",
            )
        )

    # 5. Foundation Gap (Overall struggling across the board)
    if total_att >= 3 and data.get("mastery_score", 0) < 45.0:
        weaknesses.append(
            WeaknessPattern(
                pattern_type="foundation_gap",
                topic=topic_name,
                severity="high",
                summary=f"Overall mastery is low ({data.get('mastery_score', 0):.0f}%) across initial attempts.",
                actionable_tip="Pause quiz testing. Read the AI-generated study notes and review the key topic overview first.",
            )
        )

    # 6. Retention Decay (Spaced repetition overdue)
    next_rev_str = data.get("next_review")
    if next_rev_str:
        try:
            next_rev = datetime.fromisoformat(next_rev_str)
            if datetime.now(timezone.utc) > next_rev and data.get("mastery_score", 0) >= 60.0:
                weaknesses.append(
                    WeaknessPattern(
                        pattern_type="retention_decay",
                        topic=topic_name,
                        severity="medium",
                        summary="This topic is due for spaced repetition revision to consolidate long-term memory.",
                        actionable_tip="Complete a 5-question refresher flashcard deck to reset the memory decay curve.",
                    )
                )
        except Exception:
            pass

    return weaknesses


# ─── ADAPTIVE RECOMMENDATION ENGINE ──────────────────────────────────────────

def generate_recommendation(
    topic_name: str,
    data: dict,
    weaknesses: List[WeaknessPattern],
) -> LearningRecommendation:
    """
    Selects optimal difficulty and activity type with pedagogical justification.
    """
    mastery = data.get("mastery_score", 0.0)
    easy_acc = data.get("easy_accuracy", 0.0)
    med_acc = data.get("medium_accuracy", 0.0)
    hard_acc = data.get("hard_accuracy", 0.0)
    easy_att = data.get("easy_attempts", 0)

    # Check for specific weakness patterns
    has_fundamental_inconsistency = any(
        w.pattern_type == "fundamental_inconsistency" for w in weaknesses
    )
    has_advanced_struggle = any(
        w.pattern_type == "advanced_concept_struggle" for w in weaknesses
    )
    has_misconception = any(w.pattern_type == "misconception_alert" for w in weaknesses
    )
    is_due = data.get("is_due_for_review", False)

    # Priority 1: Due review
    if is_due:
        return LearningRecommendation(
            topic=topic_name,
            recommended_activity="flashcard_revision",
            recommended_difficulty="medium",
            reasoning=f"Your scheduled spaced repetition interval for '{topic_name}' has arrived. Immediate review preserves long-term recall.",
            pedagogical_goal="Prevent memory decay and strengthen retrieval pathways.",
            urgency="critical_review",
        )

    # Priority 2: Student B - Fundamental Inconsistency
    if has_fundamental_inconsistency:
        return LearningRecommendation(
            topic=topic_name,
            recommended_activity="notes_review",
            recommended_difficulty="easy",
            reasoning=f"While you succeeded on complex questions, you missed foundational definitions ({easy_acc:.0f}% accuracy). We are routing you to review core definitions to eliminate brittle knowledge.",
            pedagogical_goal="Re-anchor fundamental definitions and eliminate blind spots.",
            urgency="foundation_repair",
        )

    # Priority 3: Misconception Alert
    if has_misconception:
        return LearningRecommendation(
            topic=topic_name,
            recommended_activity="flashcard_revision",
            recommended_difficulty="easy",
            reasoning=f"You reported high confidence on questions that were incorrect. This indicates a hidden misconception rather than a careless error.",
            pedagogical_goal="Directly confront and unlearn flawed mental models.",
            urgency="foundation_repair",
        )

    # Priority 4: Student A - Advanced Concept Struggle
    if has_advanced_struggle:
        return LearningRecommendation(
            topic=topic_name,
            recommended_activity="quiz_practice",
            recommended_difficulty="medium",
            reasoning=f"You have mastered the basics ({easy_acc:.0f}% easy accuracy) but need structured practice on intermediate application before attempting hard evaluation questions.",
            pedagogical_goal="Bridge the gap between basic definitions and complex multi-variable problems.",
            urgency="skill_reinforcement",
        )

    # Priority 5: High Mastery (Ready for Mastery Challenge)
    if mastery >= 80.0 and med_acc >= 75.0:
        return LearningRecommendation(
            topic=topic_name,
            recommended_activity="mastery_challenge",
            recommended_difficulty="hard",
            reasoning=f"Mastery on '{topic_name}' has reached {mastery:.0f}%. You are ready for high-difficulty assessment to verify full topic competence.",
            pedagogical_goal="Deep-level evaluation and mastery certification.",
            urgency="enrichment",
        )

    # Priority 6: Standard Progression
    if easy_att < 2 or easy_acc < 70.0:
        return LearningRecommendation(
            topic=topic_name,
            recommended_activity="quiz_practice",
            recommended_difficulty="easy",
            reasoning="Establish initial conceptual familiarity with foundational questions.",
            pedagogical_goal="Build baseline knowledge and confidence.",
            urgency="foundation_repair",
        )
    else:
        return LearningRecommendation(
            topic=topic_name,
            recommended_activity="quiz_practice",
            recommended_difficulty="medium",
            reasoning=f"Base accuracy is stable ({easy_acc:.0f}%). Stepping up to medium difficulty to test application of concepts.",
            pedagogical_goal="Reinforce and consolidate intermediate knowledge.",
            urgency="progression",
        )


# ─── CORE LEARNING SERVICE API ────────────────────────────────────────────────

def record_question_attempt(
    session_id: str,
    document_id: str,
    attempt: QuestionAttempt,
) -> dict:
    """
    Updates the learner model with a single question attempt, performing
    Bayesian Knowledge Tracing, weighted mastery update, calibration check,
    and spaced repetition scheduling.
    """
    profile = load_raw_profile(session_id, document_id)
    profile["total_questions_attempted"] = profile.get("total_questions_attempted", 0) + 1

    topic_name = attempt.topic.strip()
    if topic_name not in profile["topics"]:
        profile["topics"][topic_name] = {
            "topic": topic_name,
            "mastery_score": 0.0,
            "bkt_p_known": DEFAULT_BKT_P_INIT,
            "confidence_score": 0.0,
            "total_attempts": 0,
            "correct_attempts": 0,
            "easy_attempts": 0,
            "easy_correct": 0,
            "easy_accuracy": 0.0,
            "medium_attempts": 0,
            "medium_correct": 0,
            "medium_accuracy": 0.0,
            "hard_attempts": 0,
            "hard_correct": 0,
            "hard_accuracy": 0.0,
            "consecutive_correct": 0,
            "consecutive_incorrect": 0,
            "overconfident_errors": 0,
            "underconfident_successes": 0,
            "ease_factor": 2.5,
            "interval_days": 1,
            "repetitions": 0,
            "last_reviewed": None,
            "next_review": None,
            "learning_status": "unstarted",
        }

    t = profile["topics"][topic_name]

    # 1. Update attempt counts
    t["total_attempts"] += 1
    if attempt.is_correct:
        t["correct_attempts"] += 1
        t["consecutive_correct"] += 1
        t["consecutive_incorrect"] = 0
    else:
        t["consecutive_incorrect"] += 1
        t["consecutive_correct"] = 0

    diff = attempt.difficulty.lower()
    if diff == "easy":
        t["easy_attempts"] += 1
        if attempt.is_correct:
            t["easy_correct"] += 1
        t["easy_accuracy"] = round((t["easy_correct"] / t["easy_attempts"]) * 100.0, 1)
    elif diff == "hard":
        t["hard_attempts"] += 1
        if attempt.is_correct:
            t["hard_correct"] += 1
        t["hard_accuracy"] = round((t["hard_correct"] / t["hard_attempts"]) * 100.0, 1)
    else:
        t["medium_attempts"] += 1
        if attempt.is_correct:
            t["medium_correct"] += 1
        t["medium_accuracy"] = round((t["medium_correct"] / t["medium_attempts"]) * 100.0, 1)

    # 2. Confidence & Calibration tracking
    if attempt.confidence is not None:
        prev_conf = t.get("confidence_score", 0.0)
        t["confidence_score"] = round(
            ((prev_conf * (t["total_attempts"] - 1)) + attempt.confidence)
            / t["total_attempts"],
            1,
        )
        if attempt.confidence >= 70.0 and not attempt.is_correct:
            t["overconfident_errors"] = t.get("overconfident_errors", 0) + 1
        elif attempt.confidence <= 45.0 and attempt.is_correct:
            t["underconfident_successes"] = t.get("underconfident_successes", 0) + 1

    # Calibration classification
    if t.get("overconfident_errors", 0) >= 2:
        t["calibration_status"] = "overconfident"
    elif t.get("underconfident_successes", 0) >= 3:
        t["calibration_status"] = "underconfident"
    elif t["total_attempts"] >= 3:
        t["calibration_status"] = "well_calibrated"
    else:
        t["calibration_status"] = "uncalibrated"

    # 3. Bayesian Knowledge Tracing (BKT) Update
    curr_bkt = t.get("bkt_p_known", DEFAULT_BKT_P_INIT)
    t["bkt_p_known"] = calculate_bkt_update(curr_bkt, attempt.is_correct, diff)

    # 4. Weighted Mastery Score Update
    mastery, status = compute_weighted_mastery(t)
    t["mastery_score"] = mastery
    t["learning_status"] = status

    # 5. Spaced Repetition (SM-2) Update
    update_spaced_repetition(t, attempt.is_correct, attempt.confidence)

    save_raw_profile(session_id, document_id, profile)
    return t


def record_batch_quiz_submission(
    submission: BatchQuizSubmission,
) -> LearnerProfileResponse:
    """Process all questions submitted in a quiz batch."""
    for attempt in submission.attempts:
        record_question_attempt(
            session_id=submission.session_id,
            document_id=submission.document_id,
            attempt=attempt,
        )

    return get_learner_profile(submission.session_id, submission.document_id)


def get_learner_profile(session_id: str, document_id: str) -> LearnerProfileResponse:
    """Builds comprehensive learner profile with analytics, weaknesses & recommendations."""
    raw = load_raw_profile(session_id, document_id)
    topic_profiles: Dict[str, TopicMasteryProfile] = {}
    all_weaknesses: List[WeaknessPattern] = []
    due_reviews: List[str] = []

    now = datetime.now(timezone.utc)
    mastery_sum = 0.0
    bkt_sum = 0.0
    total_attempts_all = 0
    total_correct_all = 0

    topics_dict = raw.get("topics", {})

    for t_name, data in topics_dict.items():
        # Check review schedule
        is_due = False
        next_rev_str = data.get("next_review")
        if next_rev_str:
            try:
                next_rev = datetime.fromisoformat(next_rev_str)
                if now >= next_rev:
                    is_due = True
                    due_reviews.append(t_name)
            except Exception:
                pass
        data["is_due_for_review"] = is_due

        # Detect weaknesses
        topic_weaknesses = analyze_topic_weaknesses(t_name, data)
        all_weaknesses.extend(topic_weaknesses)
        detected_types = [w.pattern_type for w in topic_weaknesses]

        topic_profile = TopicMasteryProfile(
            topic=t_name,
            mastery_score=data.get("mastery_score", 0.0),
            bkt_p_known=data.get("bkt_p_known", DEFAULT_BKT_P_INIT),
            confidence_score=data.get("confidence_score", 0.0),
            total_attempts=data.get("total_attempts", 0),
            correct_attempts=data.get("correct_attempts", 0),
            easy_attempts=data.get("easy_attempts", 0),
            easy_correct=data.get("easy_correct", 0),
            easy_accuracy=data.get("easy_accuracy", 0.0),
            medium_attempts=data.get("medium_attempts", 0),
            medium_correct=data.get("medium_correct", 0),
            medium_accuracy=data.get("medium_accuracy", 0.0),
            hard_attempts=data.get("hard_attempts", 0),
            hard_correct=data.get("hard_correct", 0),
            hard_accuracy=data.get("hard_accuracy", 0.0),
            consecutive_correct=data.get("consecutive_correct", 0),
            consecutive_incorrect=data.get("consecutive_incorrect", 0),
            last_reviewed=datetime.fromisoformat(data["last_reviewed"]) if data.get("last_reviewed") else None,
            next_review=datetime.fromisoformat(data["next_review"]) if data.get("next_review") else None,
            interval_days=data.get("interval_days", 1),
            ease_factor=data.get("ease_factor", 2.5),
            is_due_for_review=is_due,
            learning_status=data.get("learning_status", "unstarted"),
            calibration_status=data.get("calibration_status", "uncalibrated"),
            detected_weaknesses=detected_types,
        )
        topic_profiles[t_name] = topic_profile

        mastery_sum += topic_profile.mastery_score
        bkt_sum += topic_profile.bkt_p_known
        total_attempts_all += topic_profile.total_attempts
        total_correct_all += topic_profile.correct_attempts

    topic_count = len(topic_profiles)
    overall_mastery = round(mastery_sum / topic_count, 1) if topic_count > 0 else 0.0
    overall_bkt = round(bkt_sum / topic_count, 3) if topic_count > 0 else round(DEFAULT_BKT_P_INIT, 3)
    overall_accuracy = (
        round((total_correct_all / total_attempts_all) * 100.0, 1)
        if total_attempts_all > 0
        else 0.0
    )

    # Determine primary global recommendation
    primary_rec: Optional[LearningRecommendation] = None
    if topic_profiles:
        # Prioritize topic with highest urgency weakness or lowest mastery
        candidate_topic = None
        # 1. Overdue review
        if due_reviews:
            candidate_topic = due_reviews[0]
        # 2. Fundamental inconsistency (Student B)
        elif any(w.pattern_type == "fundamental_inconsistency" for w in all_weaknesses):
            for w in all_weaknesses:
                if w.pattern_type == "fundamental_inconsistency":
                    candidate_topic = w.topic
                    break
        # 3. Lowest mastery topic that has been attempted
        else:
            sorted_by_mastery = sorted(
                topic_profiles.values(),
                key=lambda x: (x.mastery_score, -x.total_attempts),
            )
            candidate_topic = sorted_by_mastery[0].topic

        if candidate_topic and candidate_topic in topics_dict:
            t_data = topics_dict[candidate_topic]
            t_weaknesses = [w for w in all_weaknesses if w.topic == candidate_topic]
            primary_rec = generate_recommendation(candidate_topic, t_data, t_weaknesses)

    return LearnerProfileResponse(
        session_id=session_id,
        document_id=document_id,
        overall_mastery=overall_mastery,
        overall_bkt=overall_bkt,
        overall_accuracy=overall_accuracy,
        total_questions_attempted=raw.get("total_questions_attempted", 0),
        topic_profiles=topic_profiles,
        weaknesses=all_weaknesses,
        due_reviews=due_reviews,
        primary_recommendation=primary_rec,
    )


# ─── ADAPTIVE LEARNING PATH GENERATOR ─────────────────────────────────────────

def get_adaptive_learning_path(
    session_id: str,
    document_id: str,
    available_topics: Optional[List[str]] = None,
) -> LearningPathResponse:
    """
    Creates an ordered prerequisite progression DAG for the document's topics.
    Each node represents a concept with clear mastery gating (must achieve >= 60%
    mastery on prerequisite before unlocking next concept).
    """
    profile = get_learner_profile(session_id, document_id)

    # Determine topic list: union of available document topics and profile topics
    topics_list = list(available_topics or [])
    for t in profile.topic_profiles.keys():
        if t not in topics_list:
            topics_list.append(t)

    if not topics_list:
        topics_list = ["Introduction & Core Concepts", "Main Methodology", "Advanced Applications"]

    nodes: List[LearningPathNode] = []
    completed_count = 0
    current_focus: Optional[str] = None

    for i, t_name in enumerate(topics_list):
        prof = profile.topic_profiles.get(t_name)
        mastery = prof.mastery_score if prof else 0.0
        bkt = prof.bkt_p_known if prof else DEFAULT_BKT_P_INIT
        is_due = prof.is_due_for_review if prof else False

        # Prerequisites: previous topic in curriculum order
        prereqs = [topics_list[i - 1]] if i > 0 else []

        # Check if prerequisites are fulfilled (>= 60% mastery)
        prereqs_met = True
        for p in prereqs:
            p_prof = profile.topic_profiles.get(p)
            if not p_prof or p_prof.mastery_score < 60.0:
                prereqs_met = False
                break

        # Determine node status
        if is_due:
            status = "review_due"
            next_step = "Spaced review is due. Complete quick flashcards."
        elif mastery >= 80.0:
            status = "mastered"
            completed_count += 1
            next_step = "Mastered. Challenge hard quiz or move ahead."
        elif not prereqs_met and i > 0:
            status = "locked"
            next_step = f"Locked. Reach at least 60% mastery in '{prereqs[0]}' first."
        elif mastery >= 45.0:
            status = "in_progress"
            next_step = "Practice medium difficulty quiz questions."
        else:
            status = "ready"
            next_step = "Read topic notes and take a foundational quiz."

        if not current_focus and status in ("ready", "in_progress", "review_due"):
            current_focus = t_name

        nodes.append(
            LearningPathNode(
                topic=t_name,
                order_index=i + 1,
                status=status,
                mastery_score=mastery,
                bkt_p_known=bkt,
                prerequisites=prereqs,
                is_unlocked=prereqs_met or i == 0,
                recommended_next_step=next_step,
            )
        )

    return LearningPathResponse(
        session_id=session_id,
        document_id=document_id,
        nodes=nodes,
        current_focus_topic=current_focus or (topics_list[0] if topics_list else None),
        completed_topics_count=completed_count,
        total_topics_count=len(nodes),
    )

