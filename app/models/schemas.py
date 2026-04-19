from pydantic import BaseModel, Field


class PersonaSummary(BaseModel):
    id: str
    name: str
    title: str
    description: str


class PersonaChatRequest(BaseModel):
    persona_id: str | None = Field(default=None, max_length=100)
    message: str = Field(..., min_length=1, max_length=10000)


class PersonaChatResponse(BaseModel):
    reply: str
    persona_of: str


class PersonasListResponse(BaseModel):
    personas: list[PersonaSummary]