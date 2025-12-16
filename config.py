import os

"""
Configuration file for Composite Microservice.
Contains IP addresses or URLs of Atomic Microservices.
Using environment variables makes it future-proof (Cloud Run / Docker).
"""

# ------------------- Microservice URLs -------------------

PATIENTS_MS_URL = os.getenv("PATIENTS_MS_URL", "http://10.128.0.3:8000")
#TRANSCRIPTIONS_MS_URL = os.getenv("TRANSCRIPTIONS_MS_URL", "http://10.128.0.7:8000")
TRANSCRIPTIONS_MS_URL = os.getenv("TRANSCRIPTIONS_MS_URL", "https://transcriptions-service-486150289333.us-central1.run.app")
SUMMARIZATION_MS_URL = os.getenv("SUMMARIZATION_MS_URL", "http://10.128.0.6:8000")

# Composite internal IP (optional)
COMPOSITE_MS_URL = os.getenv("COMPOSITE_MS_URL", "http://10.128.0.12:8000")

# UI / Proxy (External IP) (optional)
UI_BASE_URL = os.getenv("UI_BASE_URL", "http://34.71.58.225:8000")


# ------------------- General Settings -------------------

REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))  # seconds
ENV = os.getenv("ENV", "development")  # or "production"

DEBUG = ENV == "development"


def print_config():
    """Optional: Print config when app starts (debug mode only)."""
    if DEBUG:
        print("\n=== Composite Service Configuration ===")
        print(f"Patients Service:    {PATIENTS_MS_URL}")
        print(f"Transcriptions Service: {TRANSCRIPTIONS_MS_URL}")
        print(f"Summarization Service:  {SUMMARIZATION_MS_URL}")
        print(f"Composite Service:   {COMPOSITE_MS_URL}")
        print(f"UI Base URL:         {UI_BASE_URL}")
        print("=====================================\n")


#curl -i -H 'If-None-Match: W/"1763950686.0"' http://10.128.0.3:8000/patients/0257ba86-e027-4edd-b6b1-7f9e026838db
# curl "http://10.128.0.3:8000/patients?gender=male"
#curl "http://10.128.0.7:8000/transcriptions"
#curl "http://104.197.5.63:8000/transcriptions"
#curl "https://transcriptions-service-486150289333.us-central1.run.app/transcriptions"