from fastapi import APIRouter

router = APIRouter()

@router.get("/claim")
def get_claim():
    return {"message": "Claim endpoint"}