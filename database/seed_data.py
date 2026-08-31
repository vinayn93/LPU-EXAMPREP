"""
LPU ExamPrep AI — Database Seeder Module
Populates the complete official Lovely Professional University (LPU) B.Tech CSE Curriculum (Terms 1 to 8 across all 4 Years).
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.models.sql_models import (
    Base, RoleSQL, ProgramSQL, AcademicYearSQL, SemesterSQL,
    UserSQL, SubjectSQL, UnitSQL, QuestionSQL, ResourceSQL
)
from backend.app.utils.auth_utils import hash_password

import tempfile

db_dir = os.path.dirname(os.path.abspath(__file__))
if os.environ.get("VERCEL") or not os.access(db_dir, os.W_OK):
    DB_PATH = os.path.join(tempfile.gettempdir(), "lpu_examprep.db")
else:
    DB_PATH = os.path.join(db_dir, "lpu_examprep.db")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_database():
    print("[DB Seeder] Initializing full official LPU B.Tech CSE curriculum database...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Roles
        if db.query(RoleSQL).count() == 0:
            print("[DB Seeder] Seeding System Roles...")
            roles = [
                RoleSQL(role_id=1, role_name="STUDENT"),
                RoleSQL(role_id=2, role_name="FACULTY"),
                RoleSQL(role_id=3, role_name="ADMIN")
            ]
            db.add_all(roles)
            db.commit()

        # 2. Programs
        if db.query(ProgramSQL).count() == 0:
            print("[DB Seeder] Seeding Academic Programs...")
            programs = [
                ProgramSQL(program_id=1, program_code="BTECH_CSE", program_name="B.Tech Computer Science & Engineering", department="School of Computer Science & Engineering"),
                ProgramSQL(program_id=2, program_code="BCA", program_name="Bachelor of Computer Applications", department="School of Computer Applications"),
                ProgramSQL(program_id=3, program_code="BSC_IT", program_name="B.Sc Information Technology", department="School of Computer Science"),
            ]
            db.add_all(programs)
            db.commit()

        # 3. Academic Years (4 Years) & Semesters (8 Terms)
        if db.query(AcademicYearSQL).count() == 0:
            print("[DB Seeder] Seeding 4 Academic Years and 8 Terms...")
            years = [
                AcademicYearSQL(year_id=1, year_number=1, year_title="1st Year (Terms 1 & 2)"),
                AcademicYearSQL(year_id=2, year_number=2, year_title="2nd Year (Terms 3 & 4)"),
                AcademicYearSQL(year_id=3, year_number=3, year_title="3rd Year (Terms 5 & 6)"),
                AcademicYearSQL(year_id=4, year_number=4, year_title="4th Year (Terms 7 & 8)"),
            ]
            db.add_all(years)
            db.commit()

            semesters = [
                SemesterSQL(semester_id=1, year_id=1, semester_number=1, semester_name="1st Year – Autumn Term"),
                SemesterSQL(semester_id=2, year_id=1, semester_number=2, semester_name="1st Year – Spring Term"),
                SemesterSQL(semester_id=3, year_id=2, semester_number=3, semester_name="2nd Year – Autumn Term"),
                SemesterSQL(semester_id=4, year_id=2, semester_number=4, semester_name="2nd Year – Spring Term"),
                SemesterSQL(semester_id=5, year_id=3, semester_number=5, semester_name="3rd Year – Autumn Term"),
                SemesterSQL(semester_id=6, year_id=3, semester_number=6, semester_name="3rd Year – Spring Term"),
                SemesterSQL(semester_id=7, year_id=4, semester_number=7, semester_name="4th Year – Autumn Term"),
                SemesterSQL(semester_id=8, year_id=4, semester_number=8, semester_name="4th Year – Spring Term"),
            ]
            db.add_all(semesters)
            db.commit()

        # 4. Users
        if db.query(UserSQL).count() == 0:
            print("[DB Seeder] Seeding Default Users...")
            pwd = hash_password("password123")
            users = [
                UserSQL(user_id=1, full_name="LPU Admin", email="admin@lpu.in", hashed_password=pwd, role_id=3, program_id=1),
                UserSQL(user_id=2, full_name="Aarav Sharma", email="aarav@lpu.in", hashed_password=pwd, role_id=1, program_id=1, registration_number="12204891"),
                UserSQL(user_id=3, full_name="Sneha Verma", email="sneha@lpu.in", hashed_password=pwd, role_id=1, program_id=1, registration_number="12205102"),
            ]
            db.add_all(users)
            db.commit()

        # 5. Complete LPU B.Tech CSE Term-Wise Syllabus (Terms 1 to 8)
        if db.query(SubjectSQL).count() == 0:
            print("[DB Seeder] Seeding Full Official LPU B.Tech CSE Subjects Across All 8 Terms...")
            
            official_subjects = [
                # Term 1 (1st Year Autumn)
                SubjectSQL(subject_id=101, program_id=1, semester_id=1, subject_code="ECE101", subject_name="Basic Electrical and Electronics Engineering", credits=4, description="Circuits, AC analysis, transformers, diodes, transistors, and logic gates."),
                SubjectSQL(subject_id=102, program_id=1, semester_id=1, subject_code="ECE102", subject_name="Basic Electrical and Electronics Engineering Lab", credits=2, description="Practical lab experiments for electrical circuits and electronic components."),
                SubjectSQL(subject_id=103, program_id=1, semester_id=1, subject_code="PHY110", subject_name="Engineering Physics", credits=4, description="Quantum mechanics, optics, lasers, fiber optics, and semiconductor physics."),
                SubjectSQL(subject_id=104, program_id=1, semester_id=1, subject_code="INT108", subject_name="Internet Programming Laboratory", credits=2, description="HTML5, CSS3, JavaScript, web forms, and DOM manipulation lab."),
                SubjectSQL(subject_id=105, program_id=1, semester_id=1, subject_code="MTH108", subject_name="Mathematics for Engineers", credits=4, description="Calculus, linear algebra, matrices, eigenvalues, and infinite series."),
                SubjectSQL(subject_id=106, program_id=1, semester_id=1, subject_code="CSE101", subject_name="Orientation to Computing-I", credits=2, description="Computer fundamentals, binary systems, hardware architecture, and software basics."),
                SubjectSQL(subject_id=107, program_id=1, semester_id=1, subject_code="INT102", subject_name="Python Programming", credits=4, description="Python syntax, control flow, functions, modules, OOP, and data handling from Year 1."),

                # Term 2 (1st Year Spring)
                SubjectSQL(subject_id=108, program_id=1, semester_id=2, subject_code="CSE202", subject_name="Computer Programming", credits=4, description="C programming, pointers, arrays, dynamic memory allocation, and file handling."),
                SubjectSQL(subject_id=109, program_id=1, semester_id=2, subject_code="CSE305", subject_name="Database Management Systems", credits=4, description="Relational data model, SQL queries, ER diagrams, normalization (3NF/BCNF), transactions."),
                SubjectSQL(subject_id=110, program_id=1, semester_id=2, subject_code="MTH208", subject_name="Differential Equations and Vector Calculus", credits=4, description="ODE, PDE, Laplace transforms, gradient, divergence, and curl."),
                SubjectSQL(subject_id=111, program_id=1, semester_id=2, subject_code="MEC107", subject_name="Engineering Drawing with AutoCAD", credits=2, description="Engineering graphics, orthographic projections, and 2D/3D AutoCAD drafting."),
                SubjectSQL(subject_id=112, program_id=1, semester_id=2, subject_code="PES101", subject_name="Environmental Studies", credits=2, description="Ecology, biodiversity, environmental pollution, conservation, and sustainable development."),
                SubjectSQL(subject_id=113, program_id=1, semester_id=2, subject_code="ENG101", subject_name="Language Elective 1 (Communication Skills)", credits=3, description="Professional English, technical writing, presentation skills, and vocabulary."),
                SubjectSQL(subject_id=114, program_id=1, semester_id=2, subject_code="CSE102", subject_name="Orientation to Computing-II", credits=2, description="Linux CLI essentials, version control with Git, shell scripting, and developer tools."),
                SubjectSQL(subject_id=115, program_id=1, semester_id=2, subject_code="CSE320", subject_name="Software Engineering", credits=4, description="Software development lifecycles (Agile/Waterfall), requirement analysis, UML diagrams, testing."),

                # Term 3 (2nd Year Autumn)
                SubjectSQL(subject_id=116, program_id=1, semester_id=3, subject_code="COMM301", subject_name="Community Development Project", credits=2, description="Social impact projects, community engagement, and engineering for societal solutions."),
                SubjectSQL(subject_id=117, program_id=1, semester_id=3, subject_code="CSE310", subject_name="Computer Networks", credits=4, description="OSI model, TCP/IP protocol suite, routing algorithms, subnets, and network security."),
                SubjectSQL(subject_id=118, program_id=1, semester_id=3, subject_code="CSE205", subject_name="Data Structures and Algorithms", credits=4, description="Arrays, linked lists, stacks, queues, trees, heaps, priority queues, graphs, searching, sorting."),
                SubjectSQL(subject_id=119, program_id=1, semester_id=3, subject_code="DES101", subject_name="Design Thinking", credits=2, description="Human-centered design, ideation, prototyping, empathy mapping, and innovation techniques."),
                SubjectSQL(subject_id=120, program_id=1, semester_id=3, subject_code="MTH302", subject_name="Discrete Mathematics", credits=4, description="Set theory, logic, relations, functions, graph theory, combinatorics, algebraic structures."),
                SubjectSQL(subject_id=121, program_id=1, semester_id=3, subject_code="INT201", subject_name="Internetworking Essentials", credits=3, description="Routers, switches, VLANs, NAT, DHCP, packet tracing, and Cisco networking principles."),
                SubjectSQL(subject_id=122, program_id=1, semester_id=3, subject_code="ENG102", subject_name="Language Elective 2", credits=3, description="Advanced communication, foreign languages (French/German/Spanish/Japanese), public speaking."),
                SubjectSQL(subject_id=123, program_id=1, semester_id=3, subject_code="CSE207", subject_name="Object Oriented Programming (C++)", credits=4, description="Classes, objects, inheritance, polymorphism, encapsulation, templates, exception handling."),
                SubjectSQL(subject_id=124, program_id=1, semester_id=3, subject_code="INT301", subject_name="Virtualisation and Cloud Computing", credits=4, description="Hypervisors, VMs, AWS/Azure cloud models (IaaS, PaaS, SaaS), containers, Docker, Kubernetes."),

                # Term 4 (2nd Year Spring)
                SubjectSQL(subject_id=125, program_id=1, semester_id=4, subject_code="APT101", subject_name="Aptitude Elective 1", credits=3, description="Quantitative aptitude, logical reasoning, verbal ability, and competitive exam prep."),
                SubjectSQL(subject_id=126, program_id=1, semester_id=4, subject_code="CSE316", subject_name="Operating Systems", credits=4, description="Process management, threads, CPU scheduling, semaphores, deadlocks, memory management, virtual memory."),
                SubjectSQL(subject_id=127, program_id=1, semester_id=4, subject_code="CSE317", subject_name="Operating Systems Laboratory", credits=2, description="Linux system calls, process creation (fork), IPC, CPU scheduling & page replacement algorithms lab."),
                SubjectSQL(subject_id=128, program_id=1, semester_id=4, subject_code="CSE325", subject_name="Computer Organisation and Design", credits=4, description="ALU, CPU registers, instruction set architecture (MIPS/RISC-V), memory hierarchy, cache, pipelining."),
                SubjectSQL(subject_id=129, program_id=1, semester_id=4, subject_code="INT401", subject_name="Artificial Intelligence Essentials", credits=4, description="Problem solving, state-space search (A*), knowledge representation, expert systems, ML basics."),
                SubjectSQL(subject_id=130, program_id=1, semester_id=4, subject_code="MTH401", subject_name="Probability and Statistics", credits=4, description="Random variables, probability distributions (Normal/Binomial/Poisson), hypothesis testing, regression."),
                SubjectSQL(subject_id=131, program_id=1, semester_id=4, subject_code="CSE306", subject_name="Programming in Java", credits=4, description="Java SE, multithreading, collections framework, JVM architecture, JDBC database connectivity, streams."),
                SubjectSQL(subject_id=132, program_id=1, semester_id=4, subject_code="EMN201", subject_name="Engineering Minor Elective 1", credits=3, description="Specialised elective course in technical domain."),

                # Term 5 (3rd Year Autumn)
                SubjectSQL(subject_id=133, program_id=1, semester_id=5, subject_code="CSE307", subject_name="Design and Analysis of Algorithms", credits=4, description="Asymptotic notation, divide & conquer, greedy algorithms, dynamic programming, graph algorithms, NP-completeness."),
                SubjectSQL(subject_id=134, program_id=1, semester_id=5, subject_code="LAW301", subject_name="Industry Ethics and Legal Issues", credits=3, description="Cyber laws, IP rights, patent filing, software licenses, ethics in AI and engineering practice."),
                SubjectSQL(subject_id=135, program_id=1, semester_id=5, subject_code="PEW301", subject_name="Pathway Elective 1 (Corporate Jobs / Higher Studies)", credits=4, description="Corporate readiness, advanced domain preparation, pathway specialisation."),
                SubjectSQL(subject_id=136, program_id=1, semester_id=5, subject_code="PEW302", subject_name="Pathway Elective 2", credits=4, description="Research, master's abroad, government jobs, or entrepreneurship pathway module."),

                # Term 6 (3rd Year Spring)
                SubjectSQL(subject_id=137, program_id=1, semester_id=6, subject_code="CSE312", subject_name="Formal Languages and Automation Theory", credits=4, description="Finite automata (DFA/NFA), regular expressions, context-free grammars, pushdown automata, Turing machines."),

                # Term 7 (4th Year Autumn)
                SubjectSQL(subject_id=138, program_id=1, semester_id=7, subject_code="CAP401", subject_name="Capstone Project-I", credits=6, description="Major real-world engineering team project problem statement, design, SRS, and initial prototype."),
                SubjectSQL(subject_id=139, program_id=1, semester_id=7, subject_code="IKS401", subject_name="Foundations of Indian Knowledge Systems", credits=2, description="Historical Indian scientific contributions, ancient mathematics, metallurgy, architecture, and logic."),
                SubjectSQL(subject_id=140, program_id=1, semester_id=7, subject_code="COP401", subject_name="Industry Co-op Project-I", credits=6, description="Full-semester corporate industry co-op internship engagement."),

                # Term 8 (4th Year Spring)
                SubjectSQL(subject_id=141, program_id=1, semester_id=8, subject_code="CAP402", subject_name="Capstone Project-II", credits=8, description="Final implementation, performance testing, deployment, paper publication, and evaluation."),
                SubjectSQL(subject_id=142, program_id=1, semester_id=8, subject_code="SEM401", subject_name="Comprehensive Seminar", credits=2, description="Technical paper presentation, research defense, and viva voice."),
            ]

            db.add_all(official_subjects)
            db.commit()

            # Seed Units for DBMS (CSE305)
            dbms_units = [
                UnitSQL(unit_id=1, subject_id=109, unit_number=1, unit_title="Unit 1: ER Modeling, Relational Model & Relational Algebra", exam_weightage_pct=25),
                UnitSQL(unit_id=2, subject_id=109, unit_number=2, unit_title="Unit 2: Advanced SQL Queries & Normalization (3NF/BCNF)", exam_weightage_pct=30),
                UnitSQL(unit_id=3, subject_id=109, unit_number=3, unit_title="Unit 3: Transactions, ACID Properties & Concurrency Control (2PL)", exam_weightage_pct=20),
                UnitSQL(unit_id=4, subject_id=109, unit_number=4, unit_title="Unit 4: File Indexing, B+ Trees & Dynamic Hashing", exam_weightage_pct=15),
                UnitSQL(unit_id=5, subject_id=109, unit_number=5, unit_title="Unit 5: Distributed Databases & NoSQL Systems", exam_weightage_pct=10),
            ]
            db.add_all(dbms_units)
            db.commit()

            # Seed Units for Data Structures & Algorithms (CSE205)
            dsa_units = [
                UnitSQL(unit_id=6, subject_id=118, unit_number=1, unit_title="Unit 1: Linear Data Structures (Arrays, Linked Lists, Stacks, Queues)", exam_weightage_pct=25),
                UnitSQL(unit_id=7, subject_id=118, unit_number=2, unit_title="Unit 2: Trees & Binary Search Trees (AVL, Red-Black Trees)", exam_weightage_pct=25),
                UnitSQL(unit_id=8, subject_id=118, unit_number=3, unit_title="Unit 3: Heaps & Priority Queues (Min-Heap, Max-Heap, Heap Sort)", exam_weightage_pct=25),
                UnitSQL(unit_id=9, subject_id=118, unit_number=4, unit_title="Unit 4: Graph Algorithms (BFS, DFS, Dijkstra, Prim/Kruskal)", exam_weightage_pct=25),
            ]
            db.add_all(dsa_units)
            db.commit()

        # 6. Sample Questions
        if db.query(QuestionSQL).count() == 0:
            print("[DB Seeder] Seeding Official Question Bank Records...")
            questions = [
                QuestionSQL(
                    question_id=1001, subject_id=109, unit_id=2,
                    question_text="Which normal form strictly eliminates transitive functional dependencies?",
                    option_a="1NF", option_b="2NF", option_c="3NF", option_d="BCNF",
                    correct_option="C", explanation="3NF removes transitive dependencies where a non-prime attribute depends on another non-prime attribute.",
                    difficulty="HARD", marks=2
                ),
                QuestionSQL(
                    question_id=1002, subject_id=118, unit_id=8,
                    question_text="What is the worst-case time complexity of extracting the maximum element from a Binary Max-Heap of N items?",
                    option_a="O(1)", option_b="O(log N)", option_c="O(N)", option_d="O(N log N)",
                    correct_option="B", explanation="Extracting the root element from a Binary Max-Heap requires O(log N) operations to re-heapify down.",
                    difficulty="MEDIUM", marks=2
                ),
                QuestionSQL(
                    question_id=1003, subject_id=126, unit_id=3,
                    question_text="Which CPU scheduling algorithm gives minimum average waiting time for a given set of processes?",
                    option_a="FCFS", option_b="Round Robin", option_c="SJF (Shortest Job First)", option_d="Priority Scheduling",
                    correct_option="C", explanation="Shortest Job First (SJF) is provably optimal as it minimizes average waiting time.",
                    difficulty="EASY", marks=2
                ),
            ]
            db.add_all(questions)
            db.commit()

        print("[DB Seeder] Full official LPU B.Tech CSE curriculum database seeded successfully.")

    except Exception as e:
        print(f"[DB Seeder Error] {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
