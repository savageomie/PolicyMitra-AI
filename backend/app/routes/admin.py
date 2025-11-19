from fastapi import APIRouter

router = APIRouter()


@router.get("/admin")
def get_admin():
    return {"message": "Admin endpoint"}


@router.get("/admin/stats")
def admin_stats():
    """Return static admin statistics for now."""
    data = {
        "total_chats": 1245,
        "total_surveys": 312,
        "top_queries": [
            "How to file a claim?",
            "What does my policy cover?",
            "How to renew my policy?",
            "Documents required for claim"
        ],
        "recommendation_counts": {
            "crop": 420,
            "health": 310,
            "life": 150,
            "micro": 95
        }
    }
    return data