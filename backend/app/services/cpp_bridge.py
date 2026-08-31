"""
LPU ExamPrep AI — C++ Subprocess Process Bridge
Connects Python FastAPI backend to compiled C++ Study Planner Engine.
"""

import os
import json
import subprocess
import tempfile
from typing import List, Dict, Any

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CPP_EXECUTABLE = os.path.join(PROJECT_ROOT, "cpp_planner", "study_planner_engine.exe")

def run_cpp_study_planner(topics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sends revision topics to C++ Max-Heap & Topological Graph scheduler engine.
    Returns prioritized study plan array.
    """
    if not os.path.exists(CPP_EXECUTABLE):
        print("[C++ Bridge Warning] study_planner_engine.exe binary missing. Using Python fallback sort.")
        for t in topics:
            weak = t.get("weakness_score", 5)
            pyq = t.get("pyq_frequency", 3)
            weight = t.get("unit_weightage_pct", 20)
            t["priority_score"] = (weak * 40.0) + (pyq * 25.0) + (weight * 20.0)
        return sorted(topics, key=lambda x: x["priority_score"], reverse=True)

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json", encoding="utf-8") as temp_in:
        json.dump(topics, temp_in)
        temp_in_path = temp_in.name

    temp_out_path = temp_in_path.replace(".json", "_out.json")

    try:
        cmd = [CPP_EXECUTABLE, "--json-file", temp_in_path, temp_out_path]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)

        if os.path.exists(temp_out_path):
            with open(temp_out_path, "r", encoding="utf-8") as f:
                schedule = json.load(f)
            return schedule
        else:
            print(f"[C++ Bridge Error] Output missing: {result.stderr}")
            return topics
    except Exception as e:
        print(f"[C++ Bridge Exception] Execution error: {e}")
        return topics
    finally:
        if os.path.exists(temp_in_path):
            try: os.remove(temp_in_path)
            except: pass
        if os.path.exists(temp_out_path):
            try: os.remove(temp_out_path)
            except: pass
