from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.core.prompts import build_persona_system_prompt, get_persona_or_default
from app.models.schemas import PersonaChatRequest


class LLMService:
    def _build_extra_headers(self) -> dict:
        headers = {}

        if settings.openrouter_http_referer:
            headers["HTTP-Referer"] = settings.openrouter_http_referer

        if settings.openrouter_app_name:
            headers["X-Title"] = settings.openrouter_app_name

        return headers

    def generate_persona_reply(self, payload: PersonaChatRequest) -> dict:
        selected_persona = get_persona_or_default(payload.persona_id)
        system_prompt = build_persona_system_prompt(selected_persona["id"])
        extra_headers = self._build_extra_headers()

        llm = ChatOpenAI(
            model=settings.openrouter_model,
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
            temperature=0.7,
            default_headers=extra_headers if extra_headers else None,
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=payload.message),
        ]

        result = llm.invoke(messages)
        reply_text = result.content if isinstance(result.content, str) else str(result.content)

        return {
            "reply": reply_text,
            "persona_of": selected_persona["id"],
        }


llm_service = LLMService()