from fastapi import APIRouter

router = APIRouter()

@router.get("/survey")
def get_survey():
    return {"message": "Survey endpoint"}