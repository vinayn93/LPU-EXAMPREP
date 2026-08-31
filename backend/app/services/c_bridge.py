"""
LPU ExamPrep AI — C Subprocess Process Bridge
Connects Python backend to compiled C Academic Data Manager CLI.
"""

import os
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
C_EXECUTABLE = os.path.join(PROJECT_ROOT, "c_data_manager", "exam_data_manager.exe")

def run_c_data_manager(action: str = "--benchmark", search_query: str = "") -> str:
    """Executes C CLI binary and returns terminal stdout output."""
    if not os.path.exists(C_EXECUTABLE):
        return "[C CLI Warning] exam_data_manager.exe binary not found."

    try:
        cmd = [C_EXECUTABLE]
        if action == "search" and search_query:
            cmd.extend(["--search", search_query])
        else:
            cmd.append("--benchmark")

        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        return res.stdout
    except Exception as e:
        return f"[C CLI Exception] Execution error: {e}"
