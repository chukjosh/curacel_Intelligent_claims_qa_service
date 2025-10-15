"""API route handlers."""
import time
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from app.models.schemas import AskRequest, AskResponse
from app.services.gemini_service import GeminiService
from app.services.storage_service import storage
from app.config import settings

router = APIRouter()
gemini_service = GeminiService()

@router.post("/extract")
async def extract_claim(file: UploadFile = File(...)) -> dict:
    """Extract medical claim information from uploaded document."""
    try:
        # Validate file type
        if file.content_type not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {settings.ALLOWED_EXTENSIONS}"
            )
        
        # Read file content
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="File is empty")
        
        # Determine file type
        file_ext = Path(file.filename).suffix.lower()
        file_type = "pdf" if file_ext == ".pdf" else "image"
        
        # Process document
        claim_data = gemini_service.process_document(content, file_type)
        
        # Store document
        doc_id = storage.save_document(claim_data, file.filename)
        
        return {
            "document_id": doc_id,
            "extracted_data": claim_data.dict()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        ) from e

@router.post("/ask")
async def ask_question(request: AskRequest) -> JSONResponse:
    """Ask a question about a previously extracted document."""
    try:
        time.sleep(2)
        
        doc_info = storage.get_document(request.document_id)
        if not doc_info:
            raise HTTPException(
                status_code=404,
                detail=f"Document with ID {request.document_id} not found"
            )
        
        claim_data = doc_info["data"]
        answer = gemini_service.answer_question(claim_data, request.question)
        
        # Return the answer as-is (already a dict with "answer" key)
        return JSONResponse(content=answer)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        ) from e


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint."""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "documents_stored": len(storage.store)
    }

@router.get("/documents")
async def list_documents() -> dict:
    """List all stored documents."""
    return storage.list_documents()
