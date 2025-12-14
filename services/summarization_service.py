import requests
from config import SUMMARIZATION_MS_URL, REQUEST_TIMEOUT


# -----------------------------
# GET /summarizations/{id}
# -----------------------------
def get_summarization(summarization_id: int):
    try:
        r = requests.get(
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
# POST /summarizations
# -----------------------------
def create_summarization(input_text: str, summary: str):
    try:
        r = requests.post(
            f"{SUMMARIZATION_MS_URL}/summarizations",
            params={"input_text": input_text, "summary": summary},
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.RequestException as e:
        return {"error": "Summarization service unreachable", "details": str(e)}

    if r.status_code == 201:
        return {"status": "success", "data": r.json()}

    return {"error": f"Unexpected response: {r.status_code}", "details": r.text}


# -----------------------------
# PUT /summarizations/{id}
# -----------------------------
def update_summarization(summarization_id: int, summary: str):
    try:
        r = requests.put(
            f"{SUMMARIZATION_MS_URL}/summarizations/{summarization_id}",
            params={"summary": summary},
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
# POST /summarizations/async
# -----------------------------
def create_async_summarization(input_text: str):
    try:
        r = requests.post(
            f"{SUMMARIZATION_MS_URL}/summarizations/async",
            params={"input_text": input_text},
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
