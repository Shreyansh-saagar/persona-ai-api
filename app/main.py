from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.persona import router as persona_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Persona AI backend powered by FastAPI, LangChain, and OpenRouter",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "https://persona-ai-ui-five.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Persona AI API is running",
        "docs": "/docs",
    }


app.include_router(health_router, prefix="/api/v1")
app.include_router(persona_router, prefix="/api/v1")