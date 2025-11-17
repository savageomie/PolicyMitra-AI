from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
from ..services.pdf_parser import extract_text_from_pdf
from ..services.llm import summarize_policy
from ..services.tts import synthesize_tts

router = APIRouter()

@router.post("/policy/simplify")
async def simplify_policy(pdf: UploadFile = File(...)):
    # 1. Accept PDF UploadFile
    if not pdf.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    file_bytes = await pdf.read()

    # 2. Extract text from PDF
    text = await extract_text_from_pdf(file_bytes)
    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

    # 3. Summarize policy
    summary_result = await summarize_policy(text)
    summary = summary_result.get("summary", "")
    explanation = summary_result.get("eli5", "")

    # 4. Generate TTS audio for explanation
    tts_audio_path = await synthesize_tts(explanation, lang="en")
    # Optionally, convert file path to URL if serving statically
    tts_audio_url = tts_audio_path.replace(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "audio")), "/audio").replace("\\", "/") if tts_audio_path != "tts_error" else "tts_error"

    # 5. Return summary, exclusions[], explanation, tts_audio_url
    # Exclusions extraction is not implemented, so return empty list for now
    return JSONResponse({
        "summary": summary,
        "exclusions": [],
        "explanation": explanation,
        "tts_audio_url": tts_audio_url
    })