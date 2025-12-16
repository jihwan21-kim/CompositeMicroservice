import requests
from config import SUMMARIZATION_MS_URL, REQUEST_TIMEOUT


# -----------------------------
# GET /summarizations (collection)
# -----------------------------
def get_summarizations(patient_id: str | None = None, limit: int = 10, offset: int = 0):
    params = {"limit": limit, "offset": offset}
    if patient_id:
        params["patient_id"] = patient_id

    try:
        r = requests.get(
            f"{SUMMARIZATION_MS_URL}/summarizations",
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.RequestException as e:
        return {"error": "Summarization service unreachable", "details": str(e)}

    if r.status_code == 200:
        return {"status": "success", "data": r.json()}

    if r.status_code == 404:
        return {"error": "No summarizations found"}

    return {"error": f"Unexpected response: {r.status_code}", "details": r.text}


# -----------------------------
# POST /summarizations
# -----------------------------
def create_summarization(patient_id: str, input_text: str):
    try:
        r = requests.post(
            f"{SUMMARIZATION_MS_URL}/summarizations",
            params={
                "patient_id": patient_id,
                "input_text": input_text
            },
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.RequestException as e:
        return {"error": "Summarization service unreachable", "details": str(e)}

    if r.status_code == 201:
        return {"status": "success", "data": r.json()}

    return {"error": f"Unexpected response: {r.status_code}", "details": r.text}


# -----------------------------
# PUT /patients/{patient_id}/summarizations/{summarization_id}
# -----------------------------
def update_summarization_for_patient(
    patient_id: str,
    summarization_id: int,
    summary: str
):
    try:
        r = requests.put(
            f"{SUMMARIZATION_MS_URL}/patients/{patient_id}/summarizations/{summarization_id}",
            params={"summary": summary},
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.RequestException as e:
        return {"error": "Summarization service unreachable", "details": str(e)}

    if r.status_code == 200:
        return {"status": "success", "data": r.json()}

    if r.status_code == 404:
        return {"error": "Summarization not found for this patient"}

    return {"error": f"Unexpected response: {r.status_code}", "details": r.text}


# -----------------------------
# PUT /summarizations/{summarization_id}
# -----------------------------
def update_summarization(
    summarization_id: int,
    input_text: str,
    summary: str
):
    payload = {
        "input_text": input_text,
        "summary": summary
    }

    try:
        r = requests.put(
            f"{SUMMARIZATION_MS_URL}/summarizations/{summarization_id}",
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.RequestException as e:
        return {"error": "Summarization service unreachable", "details": str(e)}

    if r.status_code == 200:
        return {"status": "success", "data": r.json()}

    if r.status_code == 404:
        return {"error": "Summarization not found"}

    return {"error": f"Unexpected response: {r.status_code}", "details": r.text}


# -----------------------------
# DELETE /summarizations/{id}
# -----------------------------
def delete_summarization(summarization_id: int):
    try:
        r = requests.delete(
            f"{SUMMARIZATION_MS_URL}/summarizations/{summarization_id}",
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.RequestException as e:
        return {"error": "Summarization service unreachable", "details": str(e)}

    if r.status_code == 200:
        return {"status": "success", "data": r.json()}

    if r.status_code == 404:
        return {"error": "Summarization not found"}

    return {"error": f"Unexpected response: {r.status_code}", "details": r.text}


# -----------------------------
# DELETE /summarizations/patient/{patient_id}
# -----------------------------
def delete_summaries_by_patient(patient_id: str):
    try:
        r = requests.delete(
            f"{SUMMARIZATION_MS_URL}/summarizations/patient/{patient_id}",
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.RequestException as e:
        return {"error": "Summarization service unreachable", "details": str(e)}

    if r.status_code == 200:
        return {"status": "success", "data": r.json()}

    if r.status_code == 404:
        return {"error": "No summaries found for this patient"}

    return {"error": f"Unexpected response: {r.status_code}", "details": r.text}


# -----------------------------
# POST /summarizations/async
# -----------------------------
def create_async_summarization(patient_id: str, input_text: str):
    try:
        r = requests.post(
            f"{SUMMARIZATION_MS_URL}/summarizations/async",
            params={
                "patient_id": patient_id,
                "input_text": input_text
            },
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.RequestException as e:
        return {"error": "Summarization service unreachable", "details": str(e)}

    if r.status_code == 202:
        return {"status": "accepted", "data": r.json()}

    return {"error": f"Unexpected response: {r.status_code}", "details": r.text}


# -----------------------------
# GET /jobs/{job_id}
# -----------------------------
def get_job_status(job_id: str):
    try:
        r = requests.get(
            f"{SUMMARIZATION_MS_URL}/jobs/{job_id}",
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.RequestException as e:
        return {"error": "Summarization service unreachable", "details": str(e)}

    if r.status_code == 200:
        return {"status": "success", "data": r.json()}

    if r.status_code == 404:
        return {"error": "Job not found"}

    return {"error": f"Unexpected response: {r.status_code}", "details": r.text}
