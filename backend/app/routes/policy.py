from fastapi import APIRouter

router = APIRouter()

@router.get("/policy")
def get_policy():
    return {"message": "Policy endpoint"}