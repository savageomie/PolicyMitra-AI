from fastapi import APIRouter, HTTPException
from fastapi import status
from typing import Dict, Any

router = APIRouter()


CLAIM_GUIDES: Dict[str, Dict[str, Any]] = {
    "crop": {
        "checklist": [
            "Policy document / policy number",
            "Field damage photos",
            "Farmer ID (Aadhaar)",
            "Crop details and area proof"
        ],
        "steps": [
            "Notify insurer within specified claim period",
            "Submit claim form with incident details",
            "Upload photos and farmer ID",
            "Insurer schedules survey/inspection",
            "Receive claim adjudication and payout"
        ],
        "exclusions": [
            "Losses due to wilful negligence",
            "Pre-existing crop disease not disclosed",
            "Damage outside policy period"
        ],
        "expected_time": "7-21 days (depends on inspection)",
        "required_documents": [
            "Policy copy",
            "Aadhaar or ID proof",
            "Field photos",
            "Land ownership or lease proof"
        ]
    },
    "health": {
        "checklist": [
            "Policy card / number",
            "Hospital discharge summary",
            "Medical bills and receipts",
            "Doctor's prescriptions and reports"
        ],
        "steps": [
            "Inform insurer and obtain pre-authorization if required",
            "Get claim form and fill it",
            "Attach medical reports, bills and discharge summary",
            "Submit to insurer or TPAs for processing",
            "Insurer verifies and settles per policy terms"
        ],
        "exclusions": [
            "Cosmetic treatments (unless covered)",
            "Pre-existing conditions not disclosed (subject to waiting period)",
            "Self-inflicted injuries"
        ],
        "expected_time": "10-30 days (may vary for cashless or reimbursement)",
        "required_documents": [
            "Policy copy",
            "Hospital bills & receipts",
            "Discharge summary",
            "Doctor's prescriptions and test reports",
            "Identity proof"
        ]
    },
    "life": {
        "checklist": [
            "Original policy document",
            "Death certificate (for nominee claims)",
            "Claimant's identity and relationship proof",
            "Bank account details for payout"
        ],
        "steps": [
            "Intimate insurer with policy number and claimant details",
            "Submit death certificate and claimant ID proofs",
            "Fill claim forms and provide bank details",
            "Insurer verifies and processes documents",
            "Payout to nominee as per policy terms"
        ],
        "exclusions": [
            "Death due to suicide within waiting period",
            "Fraudulent claims",
            "Non-disclosure of critical information"
        ],
        "expected_time": "30-60 days (may take longer for investigations)",
        "required_documents": [
            "Original policy document",
            "Death certificate",
            "Claimant ID and relationship proof",
            "Bank account proof (cancelled cheque)"
        ]
    }
}


@router.get("/claim/guide")
async def get_claim_guide(policy_type: str):
    """Return claim guide for the given policy_type (crop, health, life)."""
    key = (policy_type or "").strip().lower()
    guide = CLAIM_GUIDES.get(key)
    if not guide:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported policy_type. Use 'crop', 'health' or 'life'.")
    return {"policy_type": key, "guide": guide}