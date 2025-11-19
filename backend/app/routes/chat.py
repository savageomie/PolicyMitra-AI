from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from ..models.schemas import ChatRequest, ChatResponse
from ..services.llm import generate_chat_response
from ..services.tts import synthesize_tts
import os

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if request.language not in ("en", "hi"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported language")

    # Generate chat response using LLM
    # our LLM helper expects (message, context). Pass session and language inside context.
    llm_context = {
        "session_id": request.session_id,
        "language": request.language,
        "conversation": request.context,
    }
    response_text = await generate_chat_response(request.message, context=llm_context)

    # Synthesize TTS audio
    tts_audio_path = await synthesize_tts(response_text, request.language)

    # convert absolute file path to a URL under /audio if synthesis succeeded
    if tts_audio_path != "tts_error":
        audio_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "audio"))
        try:
            tts_audio_url = tts_audio_path.replace(audio_dir, "/audio").replace("\\", "/")
        except Exception:
            tts_audio_url = tts_audio_path
    else:
        tts_audio_url = "tts_error"

    return ChatResponse(
        session_id=request.session_id,
        response=response_text,
        language=request.language,
        tts_audio=tts_audio_url,
        context=request.context
    )