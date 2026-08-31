from fastapi import APIRouter, Depends
from typing import Optional

from backend.app.services.c_bridge import run_c_data_manager
from backend.app.utils.auth_utils import get_current_user_payload

router = APIRouter(prefix="/admin-cli", tags=["C Academic Data Manager Console"])

@router.get("/execute")
def execute_c_admin_tool(action: str = "benchmark", search_query: Optional[str] = None, payload: dict = Depends(get_current_user_payload)):
    """
    Executes C CLI binary (exam_data_manager.exe) performing Quicksort, searching, and CSV exports.
    """
    if action == "search" and search_query:
        stdout = run_c_data_manager("search", search_query)
    else:
        stdout = run_c_data_manager("--benchmark")

    return {
        "action": action,
        "search_query": search_query,
        "stdout_output": stdout
    }
