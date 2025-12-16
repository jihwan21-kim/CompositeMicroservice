from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from services.composite_service import process_patient_audio
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI(
    title="Composite Microservice",
    description="Orchestrates Patient, Transcription, and Summarization services",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 개발 중엔 * OK
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process-audio", status_code=201)
async def process_audio(
    audio_file: UploadFile = File(...),
    patient: str = Form(...),
    text: str = Form(...),
    audio_filename: str = Form(...)
):
    """
    Expected payload:
    {
      "patient": { "first_name": "...", "last_name": "..." },
      "audio_filename": "...",
      "text": "..."
    }
    """
    patient_data = json.loads(patient)
    audio_content = await audio_file.read()
    payload = {
            "patient": patient_data,
            "audio_filename": audio_filename,
            "text": text
        }
    
    # Basic validation (minimum required)
    if "patient" not in payload:
        raise HTTPException(status_code=400, detail="Missing patient data")

    if "audio_filename" not in payload:
        raise HTTPException(status_code=400, detail="Missing audio_filename")

    result = process_patient_audio(payload, audio_file_content=audio_content)

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
