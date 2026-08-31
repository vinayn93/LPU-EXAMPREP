from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional

from backend.app.services.cpp_bridge import run_cpp_study_planner
from backend.app.utils.auth_utils import get_current_user_payload
from backend.app.models.oop_models import StudyPlan

router = APIRouter(prefix="/study-plan", tags=["C++ DSA Study Planner Engine"])

class GeneratePlanSchema(BaseModel):
    exam_date: str # YYYY-MM-DD
    available_hours_per_day: float = 3.5
    selected_subject_codes: Optional[List[str]] = ["CSE305", "CSE307"]

@router.post("/generate")
def generate_study_plan(plan_in: GeneratePlanSchema, payload: dict = Depends(get_current_user_payload)):
    """
    Invokes compiled C++ study_planner_engine binary with Binary Max Heap
    and Prerequisite Directed Graph to generate optimal day-by-day revision schedule.
    """
    input_topics = [
        {"topic_id": 101, "topic_name": "Normal Forms (3NF, BCNF) & Join Dependencies", "subject_name": "DBMS", "unit_name": "Unit 2", "weakness_score": 9, "pyq_frequency": 8, "unit_weightage_pct": 30, "days_until_exam": 7},
        {"topic_id": 102, "topic_name": "Relational Algebra & Outer Joins", "subject_name": "DBMS", "unit_name": "Unit 1", "weakness_score": 6, "pyq_frequency": 6, "unit_weightage_pct": 25, "days_until_exam": 7},
        {"topic_id": 103, "topic_name": "Concurrency Control & 2PL Locking", "subject_name": "DBMS", "unit_name": "Unit 3", "weakness_score": 8, "pyq_frequency": 5, "unit_weightage_pct": 20, "days_until_exam": 7},
        {"topic_id": 104, "topic_name": "Dynamic Programming - 0/1 Knapsack & LCS", "subject_name": "DAA", "unit_name": "Unit 3", "weakness_score": 10, "pyq_frequency": 9, "unit_weightage_pct": 35, "days_until_exam": 7},
        {"topic_id": 105, "topic_name": "Process Synchronization & Semaphores", "subject_name": "OS", "unit_name": "Unit 2", "weakness_score": 7, "pyq_frequency": 5, "unit_weightage_pct": 20, "days_until_exam": 7},
    ]

    # Execute C++ DSA Engine
    scheduled_topics = run_cpp_study_planner(input_topics)

    oop_plan = StudyPlan(plan_id=99, student_id=payload.get("user_id", 1), exam_date=plan_in.exam_date, daily_hours=plan_in.available_hours_per_day)
    oop_plan.set_schedule(scheduled_topics)

    res = oop_plan.to_dict()
    res["engine"] = "C++ Max-Heap & Topological Graph Study Planner v2.0"
    return res
