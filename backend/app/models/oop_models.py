"""
LPU ExamPrep AI — Object-Oriented Programming (OOP) Domain Models

Encapsulates core domain entities using reusable OOP principles:
Encapsulation, Inheritance, Polymorphism, and Composition.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

class User(ABC):
    """Abstract Base Class for LPU System Users."""
    def __init__(self, user_id: int, full_name: str, email: str, role: str):
        self._user_id = user_id
        self._full_name = full_name
        self._email = email
        self._role = role
        self._created_at = datetime.now(timezone.utc)

    @property
    def user_id(self) -> int: return self._user_id
    @property
    def full_name(self) -> str: return self._full_name
    @property
    def email(self) -> str: return self._email
    @property
    def role(self) -> str: return self._role

    @abstractmethod
    def get_permissions(self) -> List[str]:
        """Polymorphic method returning permission strings."""
        pass

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self._user_id,
            "full_name": self._full_name,
            "email": self._email,
            "role": self._role,
            "permissions": self.get_permissions()
        }


class Student(User):
    """Student user role implementation."""
    def __init__(self, user_id: int, full_name: str, email: str, registration_number: str, program_name: str):
        super().__init__(user_id, full_name, email, role="STUDENT")
        self.registration_number = registration_number
        self.program_name = program_name

    def get_permissions(self) -> List[str]:
        return ["VIEW_RESOURCES", "GENERATE_AI_TEST", "SUBMIT_TEST", "VIEW_STUDY_PLAN", "VIEW_ANALYTICS"]


class Admin(User):
    """Academic Administrator role implementation."""
    def __init__(self, user_id: int, full_name: str, email: str, department: str):
        super().__init__(user_id, full_name, email, role="ADMIN")
        self.department = department

    def get_permissions(self) -> List[str]:
        return ["ALL_ACCESS", "UPLOAD_RESOURCES", "MANAGE_SUBJECTS", "RUN_C_CLI", "VIEW_GLOBAL_ANALYTICS"]


class Unit:
    """Academic Subject Unit representation."""
    def __init__(self, unit_id: int, unit_number: int, unit_title: str, weightage_pct: int = 20):
        self.unit_id = unit_id
        self.unit_number = unit_number
        self.unit_title = unit_title
        self.weightage_pct = weightage_pct

    def to_dict(self) -> Dict[str, Any]:
        return {
            "unit_id": self.unit_id,
            "unit_number": self.unit_number,
            "unit_title": self.unit_title,
            "weightage_pct": self.weightage_pct
        }


class Subject:
    """Academic Subject Domain Class."""
    def __init__(self, subject_id: int, subject_code: str, subject_name: str, credits: int = 4):
        self.subject_id = subject_id
        self.subject_code = subject_code
        self.subject_name = subject_name
        self.credits = credits
        self.units: List[Unit] = []

    def add_unit(self, unit: Unit):
        self.units.append(unit)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "subject_id": self.subject_id,
            "subject_code": self.subject_code,
            "subject_name": self.subject_name,
            "credits": self.credits,
            "total_units": len(self.units),
            "units": [u.to_dict() for u in self.units]
        }


class Question:
    """Multiple Choice Question representation."""
    def __init__(self, question_id: int, text: str, options: Dict[str, str], correct_option: str, explanation: str, marks: int = 2, difficulty: str = "MEDIUM"):
        self.question_id = question_id
        self.text = text
        self.options = options
        self.correct_option = correct_option
        self.explanation = explanation
        self.marks = marks
        self.difficulty = difficulty

    def is_correct(self, user_answer: str) -> bool:
        return user_answer.strip().upper() == self.correct_option.upper()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "question_id": self.question_id,
            "text": self.text,
            "options": self.options,
            "correct_option": self.correct_option,
            "explanation": self.explanation,
            "marks": self.marks,
            "difficulty": self.difficulty
        }


class MockTest:
    """AI Mock Test Session Class."""
    def __init__(self, test_id: int, subject_code: str, questions: List[Question], duration_minutes: int = 30):
        self.test_id = test_id
        self.subject_code = subject_code
        self.questions = questions
        self.duration_minutes = duration_minutes

    def calculate_results(self, user_answers: Dict[int, str]) -> Dict[str, Any]:
        total_questions = len(self.questions)
        correct_count = 0
        score_earned = 0
        max_possible_score = sum(q.marks for q in self.questions)
        detailed_eval = []

        for q in self.questions:
            user_ans = user_answers.get(q.question_id, "")
            is_right = q.is_correct(user_ans)
            if is_right:
                correct_count += 1
                score_earned += q.marks

            detailed_eval.append({
                "question_id": q.question_id,
                "question_text": q.text,
                "user_answer": user_ans,
                "correct_option": q.correct_option,
                "is_correct": is_right,
                "explanation": q.explanation
            })

        accuracy_pct = round((correct_count / max(1, total_questions)) * 100, 1)

        return {
            "total_questions": total_questions,
            "correct_answers": correct_count,
            "score_earned": score_earned,
            "max_possible_score": max_possible_score,
            "accuracy_percentage": accuracy_pct,
            "detailed_evaluation": detailed_eval
        }


class StudyPlan:
    """Personalized C++ DSA Study Plan Object."""
    def __init__(self, plan_id: int, student_id: int, exam_date: str, daily_hours: float):
        self.plan_id = plan_id
        self.student_id = student_id
        self.exam_date = exam_date
        self.daily_hours = daily_hours
        self.schedule_items: List[Dict[str, Any]] = []

    def set_schedule(self, schedule: List[Dict[str, Any]]):
        self.schedule_items = schedule

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "student_id": self.student_id,
            "exam_date": self.exam_date,
            "daily_hours": self.daily_hours,
            "total_tasks": len(self.schedule_items),
            "schedule": self.schedule_items
        }
