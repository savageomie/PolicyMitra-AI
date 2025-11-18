from fastapi import APIRouter

router = APIRouter()

# Static survey questions returned as JSON
SURVEY_QUESTIONS = {
    "questions": [
        {"id": 1, "key": "family_size", "question": "What is your family size?"},
        {"id": 2, "key": "income", "question": "What is your monthly household income (in INR)?"},
        {"id": 3, "key": "occupation", "question": "What is your primary occupation?"},
        {"id": 4, "key": "land_size", "question": "How much agricultural land do you own (in acres)?"},
        {"id": 5, "key": "health_history", "question": "Do you have any chronic health conditions? If yes, please list."},
        {"id": 6, "key": "loan_burden", "question": "Do you have outstanding loans? Please indicate total monthly EMI (if any)."},
        {"id": 7, "key": "num_dependents", "question": "How many dependents do you have?"},
        {"id": 8, "key": "risk_concerns", "question": "What are your main risk concerns (crop failure, health, livestock, etc.)?"},
        {"id": 9, "key": "hospital_visits_freq", "question": "How often do you visit a hospital in a year?"},
        {"id": 10, "key": "livestock_ownership", "question": "Do you own livestock? If yes, specify types and count."}
    ]
}


@router.get("/survey/questions")
def get_survey_questions():
    return SURVEY_QUESTIONS


@router.get("/survey")
def get_survey():
    return {"message": "Survey endpoint"}