import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)

from backend.app.api import auth, academic, resources, ai_engine, study_plan, admin_cli, analytics
from database.seed_data import seed_database

app = FastAPI(
    title="LPU ExamPrep AI Backend API",
    description="Year-wise exam preparation, syllabus analysis, and AI mock-test platform for Lovely Professional University.",
    version="2.0.0"
)

# Enable CORS for Web/React clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    print("[LPU ExamPrep Engine] Initializing Backend Server & Database...")
    seed_database()

# Register API Routers
app.include_router(auth.router, prefix="/api")
app.include_router(academic.router, prefix="/api")
app.include_router(resources.router, prefix="/api")
app.include_router(ai_engine.router, prefix="/api")
app.include_router(study_plan.router, prefix="/api")
app.include_router(admin_cli.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")

# Serve Frontend Static Directory
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "LPU ExamPrep AI API Backend is Online!"}

@app.get("/api/health")
def health_check():
    return {
        "status": "HEALTHY",
        "system": "LPU ExamPrep AI",
        "institution": "Lovely Professional University",
        "technologies": ["Python FastAPI", "C++ Heap/Graph Planner", "C Data Manager CLI", "MS SQL Server / SQLite", "MongoDB Document Store"]
    }
