from datetime import datetime, timezone
from typing import Dict, Any, List
from uuid import uuid4

from pymongo import MongoClient

from app.config.settings import get_settings

settings = get_settings()


class MongoDBClient:
    """
    Handles MongoDB operations for:
    - document metadata
    - RAG query logs
    """

    def __init__(self):
        self.client = MongoClient(settings.mongodb_uri)
        self.db = self.client[settings.mongodb_database]

        self.documents_collection = self.db["documents"]
        self.query_logs_collection = self.db["query_logs"]

    def upsert_document_metadata(self, metadata: Dict[str, Any]) -> None:
        """
        Insert or update document metadata.
        """

        now = datetime.now(timezone.utc)

        metadata["updated_at"] = now

        if "created_at" not in metadata:
            metadata["created_at"] = now

        self.documents_collection.update_one(
            {"document_id": metadata["document_id"]},
            {"$set": metadata},
            upsert=True,
        )

    def get_all_documents(self) -> List[Dict[str, Any]]:
        """
        Return all document metadata records.
        """

        records = list(
            self.documents_collection.find(
                {},
                {"_id": 0},
            )
        )

        return records

    def get_document_by_id(self, document_id: str) -> Dict[str, Any] | None:
        """
        Return one document metadata record.
        """

        return self.documents_collection.find_one(
            {"document_id": document_id},
            {"_id": 0},
        )

    def insert_query_log(self, log_data: Dict[str, Any]) -> str:
        """
        Insert one RAG query log.
        """

        query_id = str(uuid4())

        log_data["query_id"] = query_id
        log_data["created_at"] = datetime.now(timezone.utc)

        self.query_logs_collection.insert_one(log_data)

        return query_id

    def get_recent_query_logs(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Return recent RAG query logs.
        """

        records = list(
            self.query_logs_collection.find(
                {},
                {"_id": 0},
            )
            .sort("created_at", -1)
            .limit(limit)
        )

        return records

    def get_query_log_by_id(self, query_id: str) -> Dict[str, Any] | None:
        """
        Return one RAG query log by query_id.
        """

        return self.query_logs_collection.find_one(
            {"query_id": query_id},
            {"_id": 0},
        )