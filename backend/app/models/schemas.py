from pydantic import BaseModel
from typing import Optional, Any

class ChatRequest(BaseModel):
    session_id: str
    message: str
    language: str  # 'en' or 'hi'
    context: Optional[Any] = None

class ChatResponse(BaseModel):
    session_id: str
    response: str
    language: str
    tts_audio: Optional[str] = None  # base64 or URL to audio file
    context: Optional[Any] = None


class RecommendRequest(BaseModel):
    occupation: str
    income: int
    family_size: int


class Plan(BaseModel):
    name: str
    reason: Optional[str] = None
    estimated_premium: Optional[float] = None


class RecommendResponse(BaseModel):
    plans: list[Plan]
    trust_score: float
    total_premium: float
    explanation: Optional[str] = None