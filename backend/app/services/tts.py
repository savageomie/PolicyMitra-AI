# Async TTS service using gTTS (ready for OpenAI TTS integration)
import os
import uuid
from gtts import gTTS
import asyncio

async def synthesize_tts(text: str, lang: str = "en") -> str:
    """
    Synthesize speech from text using gTTS. Returns file path or 'tts_error' on failure.
    """
    try:
        if lang not in ("en", "hi"):
            lang = "en"
        audio_dir = os.path.join(os.path.dirname(__file__), "..", "audio")
        audio_dir = os.path.abspath(audio_dir)
        os.makedirs(audio_dir, exist_ok=True)
        filename = f"tts_{uuid.uuid4().hex}.mp3"
        file_path = os.path.join(audio_dir, filename)

        def _synthesize():
            tts = gTTS(text=text, lang=lang)
            tts.save(file_path)

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _synthesize)
        return file_path
    except Exception:
        return "tts_error"