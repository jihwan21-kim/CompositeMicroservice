import requests
from uuid import UUID
from config import TRANSCRIPTIONS_MS_URL, REQUEST_TIMEOUT


# -----------------------------
# GET /transcriptions
# -----------------------------
def get_all_transcriptions():
    try:
        r = requests.get(
            f"{TRANSCRIPTIONS_MS_URL}/transcriptions",
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.RequestException as e:
        return {
            "error": "Transcription service unreachable",
            "details": str(e),
        }

    if r.status_code == 200:
        return {
            "status": "success",
            "data": r.json(),
        }

    return {
        "error": f"Unexpected response: {r.status_code}",
        "details": r.text,
    }


# -----------------------------
# GET /transcriptions/{id}
# -----------------------------
def get_transcription(trans_id: UUID):
    try:
        r = requests.get(
            f"{TRANSCRIPTIONS_MS_URL}/transcriptions/{trans_id}",
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.RequestException as e:
        return {
            "error": "Transcription service unreachable",
            "details": str(e),
        }

    if r.status_code == 200:
        return {
            "status": "success",
            "data": r.json(),
        }

    if r.status_code == 404:
        return {"error": "Transcription not found"}

    return {
        "error": f"Unexpected response: {r.status_code}",
        "details": r.text,
    }


# -----------------------------
# POST /transcriptions
# -----------------------------
def create_transcription(audio_file_path: str):
    """
    Upload audio file (multipart/form-data)
    """
    try:
        with open(audio_file_path, "rb") as f:
            files = {
                "file": (audio_file_path, f)
            }
            r = requests.post(
                f"{TRANSCRIPTIONS_MS_URL}/transcriptions",
                files=files,
                timeout=REQUEST_TIMEOUT,
            )
    except FileNotFoundError:
        return {"error": "Audio file not found"}
    except requests.exceptions.RequestException as e:
        return {
            "error": "Transcription service unreachable",
            "details": str(e),
        }

    if r.status_code == 201:
        return {
            "status": "success",
            "data": r.json(),
        }

    return {
        "error": f"Unexpected response: {r.status_code}",
        "details": r.text,
    }


# -----------------------------
# PUT /transcriptions/{id}
# -----------------------------
def update_transcription(trans_id: UUID, update_payload: dict):
    """
    update_payload may include:
    - audio_filename
    - text
    - status
    """
    if not update_payload:
        return {"error": "Update payload cannot be empty"}

    try:
        r = requests.put(
            f"{TRANSCRIPTIONS_MS_URL}/transcriptions/{trans_id}",
            json=update_payload,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.RequestException as e:
        return {
            "error": "Transcription service unreachable",
            "details": str(e),
        }

    if r.status_code == 200:
        return {
            "status": "success",
            "data": r.json(),
        }

    if r.status_code == 404:
        return {"error": "Transcription not found"}

    if r.status_code == 400:
        return {"error": "Invalid update payload"}

    return {
        "error": f"Unexpected response: {r.status_code}",
        "details": r.text,
    }


# -----------------------------
# DELETE /transcriptions/{id}
# -----------------------------
def delete_transcription(trans_id: UUID):
    try:
        r = requests.delete(
            f"{TRANSCRIPTIONS_MS_URL}/transcriptions/{trans_id}",
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.RequestException as e:
        return {
            "error": "Transcription service unreachable",
            "details": str(e),
        }

    if r.status_code == 204:
        return {"status": "success"}

    if r.status_code == 404:
        return {"error": "Transcription not found"}

    return {
        "error": f"Unexpected response: {r.status_code}",
        "details": r.text,
    }
