# app/models/transcription_model.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class Transcription(BaseModel):
    id: UUID
    audio_filename: str
    text: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
