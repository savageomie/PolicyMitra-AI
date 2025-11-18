from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from ..models.schemas import ChatRequest, ChatResponse
from ..services.llm import generate_chat_response
from ..services.tts import synthesize_tts

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
    tts_audio = await synthesize_tts(response_text, request.language)

    return ChatResponse(
        session_id=request.session_id,
        response=response_text,
        language=request.language,
        tts_audio=tts_audio,
        context=request.context
    )