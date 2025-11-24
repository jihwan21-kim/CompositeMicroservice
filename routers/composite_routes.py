# app/routers/composite_routes.py

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.composite_service import composite_transcribe_and_summarize

router = APIRouter()


@router.post(
    "/medical-summary",
    summary="Generate medical summary using patient info and audio transcription",
    description=(
        "Composite API:\n"
        "▶ Fetch patient info (Patients Microservice)\n"
        "▶ Transcribe audio (Transcriptions Microservice)\n"
        "▶ Summarize text (Summarization Microservice - async + polling)\n"
        "Returns aggregated result."
    ),
    tags=["Composite API"],
)
async def generate_medical_summary(
    patient_id: int = Form(..., description="Patient ID to validate and fetch details"),
    file: UploadFile = File(..., description="Audio file for transcription")
):
    """
    Composite endpoint:
    - Validates patient_id (foreign key)
    - Transcribes audio
    - Generates medical summary
    - Aggregates final JSON result
    """
    try:
        result = composite_transcribe_and_summarize(patient_id, file)
        return result
    except Exception as e:
        return {
            "error": "Composite processing failed",
            "details": str(e)
        }


@router.get("/test")
def test_ping():
    return {"message": "Composite routes are active!"}
