# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import composite_routes


def create_app() -> FastAPI:
    app = FastAPI(
        title="Composite Microservice",
        description=(
            "Composite service that integrates Patients, "
            "Transcription, and Summarization microservices."
        ),
        version="1.0.0",
    )

    # CORS 설정: Frontend/UI에서 접근 가능하도록
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],          # 나중에는 특정 UI 도메인만 허용해도 됨
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health Check
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "service": "composite-microservice",
            "message": "Composite service is running"
        }

    # Composite 라우터 등록
    app.include_router(
        composite_routes.router,
        prefix="/composite",
        tags=["composite"]
    )

    return app


# FastAPI APP 객체
app = create_app()


# 로컬 실행용 (GCP VM에서는 uvicorn으로 실행)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
