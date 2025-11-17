from fastapi import APIRouter

router = APIRouter()

@router.get("/admin")
def get_admin():
    return {"message": "Admin endpoint"}