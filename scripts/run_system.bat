@echo off
echo =======================================================
echo   Launching LPU ExamPrep AI Platform
echo =======================================================

cd /d "%~dp0.."

echo [Step 1] Seeding Academic Database...
py database/seed_data.py

echo [Step 2] Launching Python FastAPI Backend Server at http://localhost:8000 ...
py -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
