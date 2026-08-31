# LPU ExamPrep AI 🎓⚡

A modern multi-language exam-preparation, subject-analysis, and AI mock-test platform designed specifically for Lovely Professional University (LPU) students.

Students select their **Program → Academic Year → Semester → Subject → Unit** to access authorized study resources, syllabus notes, PYQs, AI mock tests, performance analysis, and personalized C++ DSA study plans.

---

## 🏛️ Academic Hierarchy

```text
Program (e.g. B.Tech CSE) ──► Year (e.g. Year 2) ──► Semester (e.g. Sem 4) ──► Subject (e.g. DBMS - CSE305) ──► Unit (e.g. Unit 2: Normalization)
```

---

## 🛠️ Technology Integration & Core Concepts

- **JavaScript & React (Frontend)**: Modern UI (Tailwind CSS, glassmorphism, tabs, real-time test timer, search filters, charts).
- **Python (Backend & AI Engine)**: FastAPI, JWT Bearer authentication, Role-Based Access Control (`STUDENT`, `ADMIN`), NLP syllabus topic extraction, PYQ frequency analysis, mock-test generator.
- **C++ (`study-planner-engine`)**: Priority Queue / Binary Max Heap & Directed Acyclic Graph (DAG) for prerequisite topic scheduling (Topological Sort).
- **C (`exam-data-manager`)**: High-speed C executable for Quicksort, keyword searching, and CSV question bank export.
- **MS SQL Server & SQLite (Relational DB)**: Standard T-SQL schema (`database/schema_mssql.sql`) with stored procedures (`sp_GetStudentPerformanceReport`, `sp_IdentifyWeakTopics`), indexes, views, and SQLAlchemy ORM models.
- **MongoDB (Document & AI Store)**: Unstructured store for extracted syllabus text, AI analysis outputs, mock test explanations, search logs, and feedback (with local fallback).
- **DSA & OOP**: Heaps, priority queues, graphs, linked lists, quicksort, OOP domain classes (`Student`, `Admin`, `Subject`, `Unit`, `MockTest`, `StudyPlan`).
- **Android App Support**: Progressive Web App (PWA) with service worker (`sw.js`), Android Web App Manifest, mobile touch bottom navigation bar, and native Android Studio project (`android_app/`) ready to compile into a standalone APK.

---

## 📱 Android Application Setup

### Option A: Install as Android PWA
1. Open Chrome browser on your Android mobile device.
2. Navigate to `http://<your-computer-ip>:8000`.
3. Tap **Add to Home Screen** or **Install App** to launch as a standalone Android app.

### Option B: Build Native Android APK in Android Studio
1. Open the `android_app/` folder in **Android Studio**.
2. Sync Gradle files and click **Build APK** or run directly on an Android Device / Emulator.

---

## 🚀 Running the System Locally

### 1. Compile C++ and C Binaries
Run the compiler script using MinGW `g++` and `gcc`:
```cmd
scripts\build_binaries.bat
```

### 2. Launch the System Server
Run the platform server:
```cmd
scripts\run_system.bat
```

Navigate to **http://localhost:8000** in your browser.
