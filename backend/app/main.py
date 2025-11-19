from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import chat, survey, recommend, policy, claim, form, admin

app = FastAPI()

# Enable CORS for the frontend (Vite dev server)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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