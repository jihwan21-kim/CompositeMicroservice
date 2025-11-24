# app/services/summarization_service.py

import time
import requests
from typing import Dict, Any
from app.config import SUMMARIZATION_MS_URL, REQUEST_TIMEOUT


def request_async_summarization(input_text: str) -> Dict[str, Any]:
    """Call /summarizations/async to start async summarization."""
    try:
        res = requests.post(
            f"{SUMMARIZATION_MS_URL}/summarizations/async",
            params={"input_text": input_text},
            timeout=REQUEST_TIMEOUT
        )
        if res.status_code == 202:
            return res.json()
        else:
            return {"error": f"Failed to start job: {res.text}"}
    except Exception as e:
        return {"error": "Summarization service unreachable", "details": str(e)}


def poll_summarization_job(job_id: str, retries: int = 15, delay: int = 2) -> Dict[str, Any]:
    """
    Poll /jobs/{job_id} until 'completed' or until max retries reached.
    """
    for _ in range(retries):
        try:
            res = requests.get(f"{SUMMARIZATION_MS_URL}/jobs/{job_id}", timeout=REQUEST_TIMEOUT)
            data = res.json()

            if data.get("status") == "completed":
                return data  # contains summary
            elif data.get("status") == "failed":
                return {"error": "Summarization failed"}
        except Exception as e:
            pass

        time.sleep(delay)

    return {"error": "Timeout waiting for summarization"}


def generate_summary(input_text: str) -> Dict[str, Any]:
    """
    Composite helper:
    1) 요청 보내기 (202 Accepted)
    2) job_id polling
    3) 최종 요약 결과 반환
    """
    job_response = request_async_summarization(input_text)

    if "job_id" not in job_response:
        return {"error": "Failed to create summarization job"}

    job_id = job_response["job_id"]
    final_result = poll_summarization_job(job_id)

    return {
        "job_id": job_id,
        "summary": final_result.get("summary"),
        "status": final_result.get("status")
    }
