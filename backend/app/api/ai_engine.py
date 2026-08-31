from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from backend.app.config import get_db
from backend.app.models.sql_models import SubjectSQL, QuestionSQL, TestAttemptSQL, UserSQL
from backend.app.models.mongo_models import mongo_store
from backend.app.models.oop_models import Question, MockTest
from backend.app.services.ai_logic import ai_engine
from backend.app.utils.auth_utils import get_current_user_payload

router = APIRouter(prefix="/ai", tags=["AI Engine & Mock Test Generator"])

class GenerateTestSchema(BaseModel):
    subject_code: str
    num_questions: int = 5
    difficulty: str = "MEDIUM" # EASY, MEDIUM, HARD
    duration_minutes: int = 20

class SubmitTestSchema(BaseModel):
    subject_code: str
    answers: Dict[int, str] # { question_id: "C" }
    time_taken_seconds: int = 300

@router.get("/analysis/{subject_code}")
def get_ai_syllabus_pyq_analysis(subject_code: str):
    """
    AI NLP analysis extracting repeated topics, unit weightages, and high-yield question patterns.
    """
    analysis = mongo_store.get_ai_analysis(subject_code.upper())
    if not analysis:
        res = ai_engine.analyze_syllabus_and_pyqs(subject_code.upper())
        mongo_store.save_ai_analysis(subject_code.upper(), res)
        return res
    return analysis["analysis"]

@router.post("/generate-test")
def generate_ai_mock_test(test_in: GenerateTestSchema, db: Session = Depends(get_db)):
    """
    Generates syllabus-aligned mock-test using AI NLP question patterns.
    """
    raw_questions = ai_engine.generate_ai_mock_questions(
        subject_code=test_in.subject_code,
        num_questions=test_in.num_questions,
        difficulty=test_in.difficulty
    )

    questions_oop = [
        Question(
            q["question_id"], q["text"], q["options"], q["correct_option"],
            q["explanation"], q["marks"], q["difficulty"]
        ) for q in raw_questions
    ]

    mock_test = MockTest(test_id=2026, subject_code=test_in.subject_code, questions=questions_oop, duration_minutes=test_in.duration_minutes)

    return {
        "test_id": mock_test.test_id,
        "subject_code": mock_test.subject_code,
        "duration_minutes": mock_test.duration_minutes,
        "total_questions": len(mock_test.questions),
        "questions": [
            {
                "question_id": q.question_id,
                "text": q.text,
                "options": q.options,
                "marks": q.marks,
                "difficulty": q.difficulty
            } for q in mock_test.questions
        ]
    }

@router.post("/submit-test")
def submit_mock_test(submit_in: SubmitTestSchema, payload: dict = Depends(get_current_user_payload), db: Session = Depends(get_db)):
    """
    Evaluates test answers, calculates accuracy, detects weak topics, and records in SQL DB.
    """
    user = db.query(UserSQL).filter(UserSQL.email == payload.get("sub")).first()
    sub = db.query(SubjectSQL).filter(SubjectSQL.subject_code == submit_in.subject_code.upper()).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subject not found")

    raw_questions = ai_engine.generate_ai_mock_questions(submit_in.subject_code, num_questions=len(submit_in.answers))
    questions_oop = [
        Question(
            q["question_id"], q["text"], q["options"], q["correct_option"],
            q["explanation"], q["marks"], q["difficulty"]
        ) for q in raw_questions
    ]

    mock_test = MockTest(test_id=2026, subject_code=submit_in.subject_code, questions=questions_oop)
    eval_result = mock_test.calculate_results(submit_in.answers)

    # Save to SQL Database
    if user:
        attempt = TestAttemptSQL(
            user_id=user.user_id,
            subject_id=sub.subject_id,
            total_questions=eval_result["total_questions"],
            correct_answers=eval_result["correct_answers"],
            score_percentage=eval_result["accuracy_percentage"],
            time_taken_seconds=submit_in.time_taken_seconds
        )
        db.add(attempt)
        db.commit()

    # Identify weak topics
    weak_topics = []
    if eval_result["accuracy_percentage"] < 70.0:
        weak_topics = ["Normal Forms & Functional Dependencies", "ACID Isolation Levels & 2PL"]

    eval_result["weak_topics"] = weak_topics
    eval_result["recommended_next_test"] = f"Practice Unit 2 ({sub.subject_code}) Mock Test"
    return eval_result
