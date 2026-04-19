from fastapi import APIRouter, HTTPException

from app.core.prompts import get_personas_list
from app.models.schemas import (
    PersonaChatRequest,
    PersonaChatResponse,
    PersonasListResponse,
    PersonaSummary,
)
from app.services.llm_service import llm_service

router = APIRouter(prefix="/persona", tags=["persona"])


@router.get("/list", response_model=PersonasListResponse)
def get_personas():
    personas = get_personas_list()
    return PersonasListResponse(
        personas=[PersonaSummary(**persona) for persona in personas]
    )


@router.post("/respond", response_model=PersonaChatResponse)
def persona_respond(payload: PersonaChatRequest):
    try:
        result = llm_service.generate_persona_reply(payload)
        return PersonaChatResponse(**result)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"LLM generation failed: {str(exc)}",
        )