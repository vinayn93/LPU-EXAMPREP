"""
LPU ExamPrep AI — MongoDB Document Store Engine
Handles extracted syllabus texts, AI topic analysis, mock test explanations, search logs, and feedback.
Includes automatic local JSON document store fallback if PyMongo/MongoDB daemon is offline.
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

try:
    from pymongo import MongoClient
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False

LOCAL_MONGO_STORE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "database", "mongo_documents.json"
)

class MongoDocumentStore:
    def __init__(self, connection_uri: str = "mongodb://localhost:27017", db_name: str = "lpu_examprep_docs"):
        self.db_name = db_name
        self.use_real_mongo = False
        self.client = None
        self.db = None

        if PYMONGO_AVAILABLE:
            try:
                self.client = MongoClient(connection_uri, serverSelectionTimeoutMS=1500)
                self.client.admin.command('ping')
                self.db = self.client[db_name]
                self.use_real_mongo = True
                print("[MongoDB Store] Connected to live MongoDB instance.")
            except Exception:
                self.use_real_mongo = False
                print("[MongoDB Store] MongoDB server offline. Running in Local BSON/JSON Document Fallback Mode.")
        else:
            print("[MongoDB Store] PyMongo not installed. Running in Local Document Store Mode.")

        if not self.use_real_mongo:
            self._ensure_local_store()

    def _ensure_local_store(self):
        os.makedirs(os.path.dirname(LOCAL_MONGO_STORE_PATH), exist_ok=True)
        if not os.path.exists(LOCAL_MONGO_STORE_PATH):
            initial = {
                "syllabus_extractions": {},
                "ai_analyses": {},
                "mock_test_explanations": {},
                "search_logs": [],
                "user_feedback": []
            }
            with open(LOCAL_MONGO_STORE_PATH, "w", encoding="utf-8") as f:
                json.dump(initial, f, indent=2)

    def _read_local_store(self) -> Dict[str, Any]:
        self._ensure_local_store()
        try:
            with open(LOCAL_MONGO_STORE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"syllabus_extractions": {}, "ai_analyses": {}, "mock_test_explanations": {}, "search_logs": [], "user_feedback": []}

    def _write_local_store(self, data: Dict[str, Any]):
        self._ensure_local_store()
        with open(LOCAL_MONGO_STORE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # 1. AI Syllabus & PYQ Analysis Store
    def save_ai_analysis(self, subject_code: str, analysis_data: Dict[str, Any]):
        doc = {
            "subject_code": subject_code,
            "analysis": analysis_data,
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
        if self.use_real_mongo:
            self.db.ai_analyses.update_one({"subject_code": subject_code}, {"$set": doc}, upsert=True)
        else:
            store = self._read_local_store()
            store["ai_analyses"][subject_code] = doc
            self._write_local_store(store)

    def get_ai_analysis(self, subject_code: str) -> Optional[Dict[str, Any]]:
        if self.use_real_mongo:
            res = self.db.ai_analyses.find_one({"subject_code": subject_code})
            if res: res.pop("_id", None)
            return res
        else:
            store = self._read_local_store()
            return store["ai_analyses"].get(subject_code)

    # 2. Search History & Audit Logs
    def log_search(self, user_id: int, query: str):
        log_entry = {
            "user_id": user_id,
            "query": query,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        if self.use_real_mongo:
            self.db.search_logs.insert_one(log_entry)
        else:
            store = self._read_local_store()
            store["search_logs"].append(log_entry)
            self._write_local_store(store)

    # 3. Student Feedback
    def save_feedback(self, user_id: int, subject_code: str, rating: int, comment: str):
        doc = {
            "user_id": user_id,
            "subject_code": subject_code,
            "rating": rating,
            "comment": comment,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        if self.use_real_mongo:
            self.db.user_feedback.insert_one(doc)
        else:
            store = self._read_local_store()
            store["user_feedback"].append(doc)
            self._write_local_store(store)

mongo_store = MongoDocumentStore()
