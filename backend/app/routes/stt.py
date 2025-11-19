from fastapi import APIRouter, UploadFile, HTTPException, status
from ..services.stt import transcribe_audio

router = APIRouter()


@router.post("/stt/transcribe")
async def stt_transcribe(file: UploadFile, language: str = "en"):
    if language not in ("en", "hi"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported language")
    try:
        data = await file.read()
        text = await transcribe_audio(data, language)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
