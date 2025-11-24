# app/models/patient_model.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Patient(BaseModel):
    id: str
    name: str
    age: Optional[int] = None
    medical_history: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True  # ORM 또는 dict/json 모두 지원
