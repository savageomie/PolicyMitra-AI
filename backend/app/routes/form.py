from fastapi import APIRouter

router = APIRouter()

@router.get("/form")
def get_form():
    return {"message": "Form endpoint"}