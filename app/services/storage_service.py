"""In-memory document storage service."""
import time
from datetime import datetime
from typing import Dict, Any
from app.models.schemas import ExtractedClaim

class StorageService:
    def __init__(self):
        # Pure in-memory storage
        self.store: Dict[str, Dict[str, Any]] = {}

    def save_document(self, claim_data: ExtractedClaim, filename: str) -> str:
        """Save document and return document ID."""
        doc_id = self._generate_id()
        self.store[doc_id] = {
            "data": claim_data,
            "filename": filename,
            "timestamp": datetime.now().isoformat()
        }
        return doc_id

    def get_document(self, doc_id: str) -> Dict[str, Any]:
        """Retrieve document by ID. Returns empty dict if not found."""
        return self.store.get(doc_id, {})

    def list_documents(self) -> Dict[str, Any]:
        """List all stored documents."""
        return {
            "count": len(self.store),
            "documents": [
                {
                    "document_id": doc_id,
                    "filename": info["filename"],
                    "timestamp": info["timestamp"]
                }
                for doc_id, info in self.store.items()
            ]
        }

    def _generate_id(self) -> str:
        """Generate unique document ID."""
        return f"doc_{int(time.time())}_{len(self.store)}"

# Singleton instance
storage = StorageService()
