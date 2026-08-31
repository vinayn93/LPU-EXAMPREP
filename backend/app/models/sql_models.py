"""
LPU ExamPrep AI — SQLAlchemy Relational SQL Models
Dual-compatible with Microsoft SQL Server and SQLite.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class RoleSQL(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(30), unique=True, nullable=False) # STUDENT, FACULTY, ADMIN

    users = relationship("UserSQL", back_populates="role")


class ProgramSQL(Base):
    __tablename__ = "programs"

    program_id = Column(Integer, primary_key=True, index=True)
    program_code = Column(String(20), unique=True, nullable=False)
    program_name = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)

    users = relationship("UserSQL", back_populates="program")
    subjects = relationship("SubjectSQL", back_populates="program")


class AcademicYearSQL(Base):
    __tablename__ = "academic_years"

    year_id = Column(Integer, primary_key=True, index=True)
    year_number = Column(Integer, nullable=False)
    year_title = Column(String(30), nullable=False)

    semesters = relationship("SemesterSQL", back_populates="year")


class SemesterSQL(Base):
    __tablename__ = "semesters"

    semester_id = Column(Integer, primary_key=True, index=True)
    year_id = Column(Integer, ForeignKey("academic_years.year_id"), nullable=False)
    semester_number = Column(Integer, nullable=False)
    semester_name = Column(String(30), nullable=False)

    year = relationship("AcademicYearSQL", back_populates="semesters")
    subjects = relationship("SubjectSQL", back_populates="semester")


class UserSQL(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    program_id = Column(Integer, ForeignKey("programs.program_id"), nullable=True)
    registration_number = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    role = relationship("RoleSQL", back_populates="users")
    program = relationship("ProgramSQL", back_populates="users")
    test_attempts = relationship("TestAttemptSQL", back_populates="user")


class SubjectSQL(Base):
    __tablename__ = "subjects"

    subject_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    program_id = Column(Integer, ForeignKey("programs.program_id"), nullable=False)
    semester_id = Column(Integer, ForeignKey("semesters.semester_id"), nullable=False)
    subject_code = Column(String(20), unique=True, nullable=False, index=True)
    subject_name = Column(String(120), nullable=False)
    credits = Column(Integer, default=4)
    description = Column(Text, nullable=True)

    program = relationship("ProgramSQL", back_populates="subjects")
    semester = relationship("SemesterSQL", back_populates="subjects")
    units = relationship("UnitSQL", back_populates="subject", cascade="all, delete-orphan")
    questions = relationship("QuestionSQL", back_populates="subject")


class UnitSQL(Base):
    __tablename__ = "units"

    unit_id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.subject_id"), nullable=False)
    unit_number = Column(Integer, nullable=False)
    unit_title = Column(String(150), nullable=False)
    exam_weightage_pct = Column(Integer, default=20)

    subject = relationship("SubjectSQL", back_populates="units")
    questions = relationship("QuestionSQL", back_populates="unit")


class ResourceSQL(Base):
    __tablename__ = "resources"

    resource_id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.subject_id"), nullable=False)
    unit_id = Column(Integer, ForeignKey("units.unit_id"), nullable=True)
    title = Column(String(200), nullable=False)
    resource_type = Column(String(30), nullable=False) # SYLLABUS, NOTES, PYQ, PDF, REFERENCE_LINK
    file_path_or_url = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class QuestionSQL(Base):
    __tablename__ = "questions"

    question_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    subject_id = Column(Integer, ForeignKey("subjects.subject_id"), nullable=False)
    unit_id = Column(Integer, ForeignKey("units.unit_id"), nullable=False)
    question_text = Column(Text, nullable=False)
    option_a = Column(String(255), nullable=False)
    option_b = Column(String(255), nullable=False)
    option_c = Column(String(255), nullable=False)
    option_d = Column(String(255), nullable=False)
    correct_option = Column(String(1), nullable=False) # A, B, C, D
    explanation = Column(Text, nullable=True)
    difficulty = Column(String(15), default="MEDIUM") # EASY, MEDIUM, HARD
    marks = Column(Integer, default=2)

    subject = relationship("SubjectSQL", back_populates="questions")
    unit = relationship("UnitSQL", back_populates="questions")


class TestAttemptSQL(Base):
    __tablename__ = "test_attempts"

    attempt_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.subject_id"), nullable=False)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    score_percentage = Column(Float, nullable=False)
    time_taken_seconds = Column(Integer, nullable=False)
    attempted_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("UserSQL", back_populates="test_attempts")
