# app/services/composite_service.py

import threading
from typing import Dict, Any
from fastapi import UploadFile

from services.patient_service import create_patient, get_patient_by_id
from services.transcription_service import create_transcription, get_transcription
from services.summarization_service import create_summarization
from models.patient_model import Patient


def composite_transcribe_and_summarize(patient_id: int, file: UploadFile) -> Dict[str, Any]:
    """
    Complete Composite Workflow:
    1) Fetch patient (Foreign key validation)
    2) Transcribe audio file
    3) Generate medical summary (async + polling)
    4) Aggregate all data and return final JSON
    """

    results: Dict[str, Any] = {}

    # 1️⃣ Thread to fetch patient info
    def fetch_patient():
        results["patient_result"] = get_patient_by_id(patient_id)

    # 2️⃣ Thread to transcribe audio
    def fetch_transcription():
        results["transcription_text"] = get_transcription(file)

    # 3️⃣ Patient & Transcription 병렬 실행
    t1 = threading.Thread(target=fetch_patient)
    t2 = threading.Thread(target=fetch_transcription)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # 4️⃣ Foreign key 검증 (Patient 존재 확인)
    patient_result = results.get("patient_result")
    if not patient_result or patient_result.get("error"):
        return {
            "error": "Invalid patient_id (Foreign key constraint)",
            "details": patient_result,
        }

    # Pydantic 모델로 변환 (정확하고 안전하게 사용 가능)
    patient_data = Patient.model_validate(patient_result["data"])
    transcription_text = results.get("transcription_text")

    if not transcription_text:
        return {
            "error": "Failed to transcribe audio file",
            "details": results.get("transcription_text")
        }

    # 5️⃣ Summarization microservice 호출 (Async + polling)
    summary_result = get_summarization(transcription_text)

    # 6️⃣ 최종 응답 Aggregation
    return {
        "patient": patient_data,
        "transcription_text": transcription_text,
        "summary": summary_result.get("summary"),
        "job_id": summary_result.get("job_id"),
        "summary_status": summary_result.get("status"),
        "note": "Composite aggregation complete"
    }

def process_patient_audio(payload: dict, audio_file_content: bytes):
    """
    payload = {
        "patient": {"first_name": "...", "last_name": "..."},
        "audio_filename": "...",
        "text": "transcription text"
    }
    """

    # -----------------------------
    # 1️⃣ Create Patient (sync)
    # -----------------------------
    patient_res = create_patient(payload["patient"])
    if "error" in patient_res:
        return patient_res

    patient_id = patient_res["data"]["id"]

    # -----------------------------
    # 2️⃣ Transcription (thread)
    # -----------------------------
    transcription_result = {}

    def transcription_worker():
        res = create_transcription(patient_id, payload["audio_filename"], audio_file_content)
        transcription_result["data"] = res

    transcription_thread = threading.Thread(target=transcription_worker)
    transcription_thread.start()
    transcription_thread.join()  # wait for completion

    transcription_res = transcription_result["data"]
    if "error" in transcription_res:
        return transcription_res

    transcription_text = transcription_res["data"]["text"]

    # -----------------------------
    # 3️⃣ Summarization (thread)
    # -----------------------------
    summarization_result = {}

    def summarization_worker():
        res = create_summarization(
            patient_id=patient_id,
            input_text=transcription_text
        )
        summarization_result["data"] = res

    summarization_thread = threading.Thread(target=summarization_worker)
    summarization_thread.start()
    summarization_thread.join()

    summarization_res = summarization_result["data"]
    if "error" in summarization_res:
        return summarization_res

    # -----------------------------
    # 4️⃣ Final Response
    # -----------------------------
    return {
        "patient_id": patient_id,
        "summary": summarization_res["data"]["summary"]
    }
