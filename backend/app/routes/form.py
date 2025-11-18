from fastapi import APIRouter, HTTPException
from ..models.schemas import FormRequest, FormAssistResponse
import re

router = APIRouter()


@router.get("/form")
def get_form():
    return {"message": "Form endpoint"}


@router.post("/form/assist", response_model=FormAssistResponse)
async def assist_form(data: FormRequest):
    """Validate required fields and provide Aadhaar correction suggestion and hints."""
    required = ["name", "aadhaar", "address", "phone", "age"]
    missing = []
    cleaned = {}
    # collect cleaned values
    for field in required:
        value = getattr(data, field, None)
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(field)
        else:
            cleaned[field] = value

    # Aadhaar validation: should be 12 digits. Accept spaces or dashes, but suggest cleaned version.
    aad = (data.aadhaar or "")
    aad_digits = re.sub(r"\D", "", aad)
    aad_valid = len(aad_digits) == 12
    aad_suggestion = None
    if aad and not aad_valid:
        if len(aad_digits) < 12:
            aad_suggestion = f"Aadhaar looks short. After removing non-digits we got '{aad_digits}'. Aadhaar must be 12 digits."
        elif len(aad_digits) > 12:
            aad_suggestion = f"Aadhaar looks long. After removing non-digits we got '{aad_digits}'. Aadhaar must be 12 digits — please verify."
        else:
            aad_suggestion = f"Please provide a 12-digit Aadhaar number. Cleaned value: '{aad_digits}'."
    elif aad and aad_valid:
        # format suggestion: grouped by 4 for readability
        formatted = " ".join([aad_digits[i:i+4] for i in range(0, 12, 4)])
        aad_suggestion = formatted
        cleaned["aadhaar"] = aad_digits

    # LLM hint (static for now)
    hints = ["Fill Aadhaar exactly as shown on card."]

    return FormAssistResponse(
        missing_fields=missing,
        aadhaar_valid=aad_valid,
        aadhaar_suggestion=aad_suggestion,
        hints=hints,
        cleaned=cleaned
    )