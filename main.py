from fastapi import FastAPI, HTTPException
from services.composite_service import process_patient_audio

app = FastAPI(
    title="Composite Microservice",
    description="Orchestrates Patient, Transcription, and Summarization services",
    version="1.0.0",
)


@app.post("/process-audio", status_code=201)
def process_audio(payload: dict):
    """
    Expected payload:
    {
      "patient": { "first_name": "...", "last_name": "..." },
      "audio_filename": "...",
      "text": "..."
    }
    """

    # Basic validation (minimum required)
    if "patient" not in payload:
        raise HTTPException(status_code=400, detail="Missing patient data")

    if "audio_filename" not in payload:
        raise HTTPException(status_code=400, detail="Missing audio_filename")

    result = process_patient_audio(payload)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result)

    return result

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "composite-microservice"
    }

@app.get("/")
def root():
    return {
        "message": "Composite Microservice is running",
        "endpoints": ["/process-audio"]
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
