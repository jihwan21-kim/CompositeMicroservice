# app/services/patient_service.py

import requests
from config import PATIENTS_MS_URL, REQUEST_TIMEOUT


def get_patient_by_id(patient_id: int, etag: str | None = None):
    """
    Calls Patients Microservice GET /patients/{id}
    Supports:
    - Foreign Key validation
    - ETag conditional requests (304 handling)
    """
    headers = {}
    if etag:
        headers["If-None-Match"] = etag

    try:
        response = requests.get(
            f"{PATIENTS_MS_URL}/patients/{patient_id}",
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.RequestException as e:
        return {"error": "Patient service unreachable", "details": str(e)}

    # 304 → Not Modified (ETag match)
    if response.status_code == 304:
        return {"status": "not_modified", "etag": etag}

    # 404 → Not Found (Foreign Key 검증 실패)
    if response.status_code == 404:
        return {"error": "Invalid patient_id (Foreign key constraint failed)"}

    # 성공 (200)
    if response.status_code == 200:
        return {
            "status": "success",
            "data": response.json(),
            "etag": response.headers.get("ETag")
        }

    # 기타 에러
    return {"error": f"Unexpected response: {response.status_code}", "details": response.text}
