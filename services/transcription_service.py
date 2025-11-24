# app/services/transcription_service.py

import requests
from typing import Dict, Any
from fastapi import UploadFile
from config import TRANSCRIPTIONS_MS_URL, REQUEST_TIMEOUT
from models.transcription_model import Transcription


def create_transcription_job(file: UploadFile) -> Dict[str, Any]:
    """
    Composite → Transcription Microservice
    POST /transcriptions (multipart/form-data with file)
    """
    files = {
        "file": (file.filename, file.file, file.content_type)
    }

    try:
        res = requests.post(
            f"{TRANSCRIPTIONS_MS_URL}/transcriptions",
            files=files,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.RequestException as e:
        return {"error": "Transcription service unreachable", "details": str(e)}

    if res.status_code != 201:
        return {"error": f"Transcription failed", "status_code": res.status_code, "details": res.text}

    # TranscriptionRead 구조를 Pydantic 모델로 검증
    data = res.json()
    transcription_obj = Transcription.model_validate(data)

    return {
        "status": "success",
        "data": transcription_obj,
    }


def get_transcription_text(file: UploadFile) -> str | None:
    """
    Convenience helper:
    - creates transcription job
    - returns only the 'text' field
    """
    result = create_transcription_job(file)

    if result.get("status") != "success":
        return None

    transcription: Transcription = result["data"]
    return transcription.text
