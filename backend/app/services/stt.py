# Async STT service for Groq and OpenAI
import os
import httpx
from typing import Optional

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

GROQ_MODEL = "whisper-large-v3"
OPENAI_MODEL = "gpt-4o-transcribe"

async def _call_groq_stt(file_bytes: bytes, language: str) -> str:
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    data = {"model": GROQ_MODEL, "language": language}
    files = {"file": ("audio.wav", file_bytes, "audio/wav")}
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(url, headers=headers, data=data, files=files)
        resp.raise_for_status()
        return resp.json().get("text", "")

async def _call_openai_stt(file_bytes: bytes, language: str) -> str:
    url = "https://api.openai.com/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    data = {"model": OPENAI_MODEL, "language": language}
    files = {"file": ("audio.wav", file_bytes, "audio/wav")}
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(url, headers=headers, data=data, files=files)
        resp.raise_for_status()
        return resp.json().get("text", "")

async def transcribe_audio(file_bytes: bytes, language: str, provider: str = "groq") -> str:
    """
    Async audio transcription for Groq and OpenAI.
    """
    try:
        if language not in ("en", "hi"):
            raise ValueError("Unsupported language")
        if provider == "groq":
            if not GROQ_API_KEY:
                raise ValueError("Missing GROQ_API_KEY")
            return await _call_groq_stt(file_bytes, language)
        elif provider == "openai":
            if not OPENAI_API_KEY:
                raise ValueError("Missing OPENAI_API_KEY")
            return await _call_openai_stt(file_bytes, language)
        else:
            raise ValueError(f"Unknown provider: {provider}")
    except Exception:
        return "Transcription error, please try again."