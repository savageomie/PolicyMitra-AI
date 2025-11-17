from fastapi import FastAPI
from .routes import chat, survey, recommend, policy, claim, form, admin

app = FastAPI()

# Include routers
app.include_router(chat.router)
app.include_router(survey.router)
app.include_router(recommend.router)
app.include_router(policy.router)
app.include_router(claim.router)
app.include_router(form.router)
app.include_router(admin.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}