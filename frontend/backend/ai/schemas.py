from typing import Literal

from pydantic import BaseModel, Field


Mode = Literal[
    "listen",
    "understand",
    "options",
    "information",
    "plan",
]

Language = Literal["en", "ur"]

class ChatRequest(BaseModel):
    session_id: str = Field(
        min_length=1,
        max_length=100,
    )

    message: str = Field(
        min_length=1,
        max_length=5000,
    )

    mode: Mode = "listen"

    language: Language = "EN"


class ChatResponse(BaseModel):
    reply: str
    risk_flag: bool
    resources_used: list[str]
    detected_emotion: str
    detected_intent: str


class HealthResponse(BaseModel):
    status: str
    provider_configured: bool