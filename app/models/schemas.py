"""Pydantic data models."""
from typing import Optional
from pydantic import BaseModel

class PatientInfo(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None

class Medication(BaseModel):
    name: Optional[str] = None
    dosage: Optional[str] = None
    quantity: Optional[str] = None

class Admission(BaseModel):
    was_admitted: bool = False
    admission_date: Optional[str] = None
    discharge_date: Optional[str] = None

class ExtractedClaim(BaseModel):
    patient: PatientInfo
    diagnoses: list[str] = []
    medications: list[Medication] = []
    procedures: list[str] = []
    admission: Admission
    total_amount: Optional[str] = None

class AskRequest(BaseModel):
    document_id: str
    question: str

class AskResponse(BaseModel):
    answer: str
