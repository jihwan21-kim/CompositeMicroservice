# app/services/patient_service.py

import requests
from config import PATIENTS_MS_URL, REQUEST_TIMEOUT

def get_all_patients(etag: str | None = None):
    """
    Calls Patients Microservice GET /patients
    Supports:
    - ETag conditional requests (304 handling)
    """
    headers = {}
    if etag:
        headers["If-None-Match"] = etag

    try:
        response = requests.get(
            f"{PATIENTS_MS_URL}/patients",
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.RequestException as e:
        return {"error": "Patient service unreachable", "details": str(e)}

    if response.status_code == 304:
        return {"status": "not_modified", "etag": etag}

    if response.status_code == 200:
        return {
            "status": "success",
            "data": response.json(),
            "etag": response.headers.get("ETag")
        }

    return {"error": f"Unexpected response: {response.status_code}", "details": response.text}

def create_patient(patient_data: dict):
    """
    Calls Patients Microservice POST /patients
    """
    try:
        response = requests.post(
            f"{PATIENTS_MS_URL}/patients",
            json=patient_data,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.RequestException as e:
        return {"error": "Patient service unreachable", "details": str(e)}

    if response.status_code in (200, 201):
        return {
            "status": "success",
            "data": response.json(),
            "etag": response.headers.get("ETag")
        }

    return {"error": f"Unexpected response: {response.status_code}", "details": response.text}

def update_patient(patient_id: str, patient_data: dict, etag: str | None = None):
    """
    Calls Patients Microservice PUT /patients/{id}
    Supports:
    - ETag optimistic concurrency control
    """
    headers = {}
    if etag:
        headers["If-Match"] = etag

    try:
        response = requests.put(
            f"{PATIENTS_MS_URL}/patients/{patient_id}",
            json=patient_data,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.RequestException as e:
        return {"error": "Patient service unreachable", "details": str(e)}

    if response.status_code == 404:
        return {"error": "Invalid patient_id"}

    if response.status_code == 412:
        return {"error": "ETag mismatch (Precondition Failed)"}

    if response.status_code == 200:
        return {
            "status": "success",
            "data": response.json(),
            "etag": response.headers.get("ETag")
        }

    return {"error": f"Unexpected response: {response.status_code}", "details": response.text}


def get_patient_by_id(patient_id: str, etag: str | None = None):
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

def delete_patient(patient_id: str, etag: str | None = None):
    """
    Calls Patients Microservice DELETE /patients/{id}
    Supports:
    - ETag conditional delete
    """
    headers = {}
    if etag:
        headers["If-Match"] = etag

    try:
        response = requests.delete(
            f"{PATIENTS_MS_URL}/patients/{patient_id}",
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.RequestException as e:
        return {"error": "Patient service unreachable", "details": str(e)}

    if response.status_code == 404:
        return {"error": "Invalid patient_id"}

    if response.status_code == 412:
        return {"error": "ETag mismatch (Precondition Failed)"}

    if response.status_code in (200, 204):
        return {"status": "success"}

    return {"error": f"Unexpected response: {response.status_code}", "details": response.text}
