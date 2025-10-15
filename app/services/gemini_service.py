"""Gemini AI service for document processing with PDF and image support."""
import json
from typing import Literal
import google.generativeai as genai

from app.config import settings
from app.models.schemas import ExtractedClaim, PatientInfo, Medication, Admission
from app.services.document_processor import DocumentProcessor  # unified processor

genai.configure(api_key=settings.GEMINI_API_KEY)

class GeminiService:
    def __init__(self):
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL_PRIMARY)

    def process_document(self, content: bytes, file_type: Literal["pdf", "image"]) -> ExtractedClaim:
        """
        Process a document (PDF or image) and extract structured data.
        """
        if file_type.lower() == "pdf":
            text = DocumentProcessor.extract_text(content, "pdf")
        else:
            text = DocumentProcessor.extract_text(content, "image")

        prompt = self._get_extraction_prompt(text)
        response = self.model.generate_content(prompt)
        return self._parse_response(response.text)

    def answer_question(self, claim_data: ExtractedClaim, question: str) -> dict:
        """
        Answer a question about the claim data.
        Returns a simple JSON like {"answer": "10 tablets"}.
        """
        document_json = json.dumps(claim_data.dict(), indent=2)
        prompt = f"""
        You are a medical assistant. Based on the medical claim data below,
        answer the question as briefly as possible.

        Medical Claim Data:
        {document_json}

        Question: {question}

        Return only the answer to the question.
        If the information is not available, reply with 'Information not available'.
        """

        response = self.model.generate_content(prompt)
        answer_text = response.text.strip()

        # Wrap the answer in a simple JSON structure
        return {"answer": answer_text}

    @staticmethod
    def _get_extraction_prompt(text: str = "") -> str:
        """Prompt to extract structured JSON from a document."""
        doc_text = f"Medical Document Text:\n{text}\n\n" if text else ""
        return f"""
        Analyze this medical claim sheet and extract structured information.

        {doc_text}Extract and return ONLY a valid JSON object with this structure:
        {{
            "patient": {{"name": "string or null","age": "number or null"}},
            "diagnoses": ["list of diagnoses"],
            "medications": [{{"name": "medication name","dosage": "dosage or null","quantity": "quantity or null"}}],
            "procedures": ["list of procedures"],
            "admission": {{"was_admitted": true/false,"admission_date": "YYYY-MM-DD or null","discharge_date": "YYYY-MM-DD or null"}},
            "total_amount": "amount with currency or null"
        }}

        Return ONLY the JSON object, no other text.
        """

    @staticmethod
    def _parse_response(json_str: str) -> ExtractedClaim:
        """Parse the Gemini JSON response into an ExtractedClaim object."""
        try:
            json_str = json_str.strip()
            if json_str.startswith("```"):
                json_str = json_str.split("```")[1]
                if json_str.startswith("json"):
                    json_str = json_str[4:]
            data = json.loads(json_str.strip())

            return ExtractedClaim(
                patient=PatientInfo(
                    name=data.get("patient", {}).get("name"),
                    age=data.get("patient", {}).get("age")
                ),
                diagnoses=data.get("diagnoses", []),
                medications=[
                    Medication(
                        name=med.get("name"),
                        dosage=med.get("dosage"),
                        quantity=med.get("quantity")
                    ) for med in data.get("medications", [])
                ],
                procedures=data.get("procedures", []),
                admission=Admission(
                    was_admitted=data.get("admission", {}).get("was_admitted", False),
                    admission_date=data.get("admission", {}).get("admission_date"),
                    discharge_date=data.get("admission", {}).get("discharge_date")
                ),
                total_amount=data.get("total_amount")
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {str(e)}") from e
