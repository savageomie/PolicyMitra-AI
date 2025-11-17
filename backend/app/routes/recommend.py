from fastapi import APIRouter

router = APIRouter()

@router.get("/recommend")
def get_recommend():
    return {"message": "Recommend endpoint"}