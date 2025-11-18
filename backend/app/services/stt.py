# Async STT service (Groq-only)
import os
import httpx

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "whisper-large-v3"

async def _call_groq_stt(file_bytes: bytes, language: str) -> str:
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    data = {"model": GROQ_MODEL, "language": language}
    files = {"file": ("audio.wav", file_bytes, "audio/wav")}
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(url, headers=headers, data=data, files=files)
        resp.raise_for_status()
        return resp.json().get("text", "")

async def transcribe_audio(file_bytes: bytes, language: str) -> str:
    """
    Async audio transcription using Groq only.
    """
    try:
        if language not in ("en", "hi"):
            raise ValueError("Unsupported language")
        if not GROQ_API_KEY:
            raise ValueError("Missing GROQ_API_KEY")
        return await _call_groq_stt(file_bytes, language)
    except Exception:
        return "Transcription error, please try again."