from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.config import get_db
from backend.app.models.sql_models import ProgramSQL, AcademicYearSQL, SemesterSQL, SubjectSQL, UnitSQL
from backend.app.models.oop_models import Subject, Unit

router = APIRouter(prefix="/academic", tags=["Academic Hierarchy Navigator & LPU Modules"])

@router.get("/programs")
def get_programs(db: Session = Depends(get_db)):
    return db.query(ProgramSQL).all()

@router.get("/years")
def get_years(db: Session = Depends(get_db)):
    years = db.query(AcademicYearSQL).all()
    results = []
    for y in years:
        sems = db.query(SemesterSQL).filter(SemesterSQL.year_id == y.year_id).all()
        results.append({
            "year_id": y.year_id,
            "year_number": y.year_number,
            "year_title": y.year_title,
            "semesters": [{"semester_id": s.semester_id, "semester_number": s.semester_number, "semester_name": s.semester_name} for s in sems]
        })
    return results

@router.get("/subjects")
def get_subjects(program_id: Optional[str] = None, semester_id: Optional[str] = None, search: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(SubjectSQL)
    if program_id and str(program_id).isdigit():
        query = query.filter(SubjectSQL.program_id == int(program_id))
    if semester_id and str(semester_id).isdigit():
        query = query.filter(SubjectSQL.semester_id == int(semester_id))
    if search and search.strip():
        query = query.filter(
            (SubjectSQL.subject_name.ilike(f"%{search.strip()}%")) | 
            (SubjectSQL.subject_code.ilike(f"%{search.strip()}%"))
        )

    subjects = query.all()
    res = []
    for s in subjects:
        oop_sub = Subject(s.subject_id, s.subject_code, s.subject_name, s.credits)
        for u in s.units:
            oop_sub.add_unit(Unit(u.unit_id, u.unit_number, u.unit_title, u.exam_weightage_pct))
        data = oop_sub.to_dict()
        data["description"] = s.description
        data["program_name"] = s.program.program_name if s.program else "General"
        data["semester_id"] = s.semester_id
        data["semester_name"] = s.semester.semester_name if s.semester else f"Term {s.semester_id}"
        res.append(data)
    return res

# 1. NEW MODULE: Core Key Areas / Subject Domains
@router.get("/domains")
def get_subject_domains():
    return [
        {
            "domain_id": "programming",
            "title": "Programming Languages & Paradigms",
            "icon": "💻",
            "subjects": ["Python Programming", "Computer Programming (C)", "Object Oriented Programming (C++)", "Programming in Java"],
            "description": "Foundational and advanced coding competencies from Year 1 Term 1."
        },
        {
            "domain_id": "data_algo",
            "title": "Data Structures & Algorithms",
            "icon": "⚡",
            "subjects": ["Data Structures and Algorithms", "Design and Analysis of Algorithms", "Discrete Mathematics"],
            "description": "Algorithmic problem solving, asymptotic efficiency, dynamic programming, and logic."
        },
        {
            "domain_id": "systems",
            "title": "Computer Systems & Cloud",
            "icon": "🖥️",
            "subjects": ["Operating Systems", "Computer Organisation and Design", "Virtualisation and Cloud Computing"],
            "description": "CPU architecture, virtual memory, process scheduling, hypervisors, Docker & AWS."
        },
        {
            "domain_id": "db_net",
            "title": "Databases & Computer Networks",
            "icon": "🗄️",
            "subjects": ["Database Management Systems", "Computer Networks", "Internetworking Essentials"],
            "description": "SQL normalization (3NF/BCNF), ACID isolation, OSI layers, TCP/IP, Cisco routing."
        },
        {
            "domain_id": "math",
            "title": "Engineering Mathematics",
            "icon": "📐",
            "subjects": ["Mathematics for Engineers", "Differential Equations and Vector Calculus", "Probability and Statistics"],
            "description": "Calculus, linear algebra, random variables, hypothesis testing, and quantitative foundations."
        },
        {
            "domain_id": "ai",
            "title": "Intelligent Systems & Soft Computing",
            "icon": "🧠",
            "subjects": ["Artificial Intelligence Essentials", "Soft Computing"],
            "description": "State-space search (A*), neural networks, fuzzy logic, genetic algorithms."
        },
        {
            "domain_id": "software_eng",
            "title": "Software Engineering & Theory",
            "icon": "🏗️",
            "subjects": ["Software Engineering", "Formal Languages and Automation Theory"],
            "description": "Agile/UML software design, DFA/NFA finite automata, Turing machines, computation theory."
        },
        {
            "domain_id": "professional",
            "title": "Professional Development & Ethics",
            "icon": "⚖️",
            "subjects": ["Industry Ethics and Legal Issues", "Foundations of Indian Knowledge Systems"],
            "description": "Cyber laws, IP rights, software licensing, and ancient Indian scientific contributions."
        }
    ]

# 2. NEW MODULE: Elective Categories Hub
@router.get("/electives")
def get_elective_categories():
    return [
        {
            "category": "Engineering Minor Electives",
            "badge": "Technical Mastery",
            "description": "Enhance competency in technical and emerging domains across Years 3 and 4.",
            "options": ["AI & Machine Learning Minor", "Cybersecurity Minor", "Cloud Computing Minor", "Data Science Minor"]
        },
        {
            "category": "Department Electives",
            "badge": "Deep Discipline Depth",
            "description": "Courses from within CSE discipline providing specialized depth.",
            "options": ["Advanced Java Programming", "Blockchain Technology", "Network Security & Cryptography", "Game Development 3D", "Linux System Administration", "Computer Graphics & Visualisation", "Software Project Management"]
        },
        {
            "category": "Language Electives",
            "badge": "Global Edge",
            "description": "Indian and foreign language options alongside communication skills.",
            "options": ["French Language & Culture", "German for Professionals", "Japanese Conversational", "Spanish Essentials", "Advanced Communication Skills"]
        },
        {
            "category": "Pathway Electives",
            "badge": "Career Path Choice",
            "description": "Aligned with career trajectories for corporate, research, or higher studies.",
            "options": ["Corporate Jobs Pathway", "Government Jobs (GATE/IES) Pathway", "Higher Studies & Masters Abroad", "Entrepreneurship & Startup Incubator", "Research & Publication Track"]
        },
        {
            "category": "Open Minors",
            "badge": "Interdisciplinary",
            "description": "Subjects outside CSE discipline for broad skill development.",
            "options": ["Management & Marketing Minor", "Digital Media & Design Minor", "Financial Technology Minor", "Robotics & Automation Minor"]
        },
        {
            "category": "Training Electives",
            "badge": "Industry Practical",
            "description": "Hands-on industry components and internship projects.",
            "options": ["Industry Co-op Project II", "Industry Internship Project", "Summer Training Seminar", "Training in Competitive Programming"]
        }
    ]

# 3. NEW MODULE: Pedagogy Pillars & 22 Industry Collaborations
@router.get("/pedagogy-partners")
def get_pedagogy_and_partners():
    return {
        "pedagogy_pillars": [
            {"title": "Practice-Based Teaching", "desc": "Learning through application rather than passive instruction."},
            {"title": "Learning by Doing", "desc": "Hands-on engagement with real tools, live code, and real engineering problems."},
            {"title": "Industry Immersion", "desc": "Direct exposure through corporate tie-ups, projects, and co-op internships."},
            {"title": "MOOCs & Certifications", "desc": "Global industry certifications integrated directly alongside the degree."},
            {"title": "Simulations & Tools", "desc": "Use of industry-standard simulation software and cloud platforms."},
            {"title": "Live Competitive Coding", "desc": "Continuous engagement on competitive coding platforms to build problem-solving speed."}
        ],
        "industry_partners": [
            "Google", "Microsoft", "Cisco", "Intel", "Informatica", "TCS", "GitHub", 
            "Honeywell", "IBM", "CompTIA", "GeeksforGeeks", "Futurense", "Kalvium", 
            "Quantiphi", "upGrad", "EC Council", "ImaginXP", "Cadence", "NASSCOM", 
            "IEEE", "AIESEC", "Institution of Engineers"
        ]
    }
