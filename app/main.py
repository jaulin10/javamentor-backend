from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth
from app.routers import chat
from app.routers import exercises
from app.database import Base, engine
from app.models import user, conversation, exercise

# Create tables
Base.metadata.create_all(bind=engine)
conversation.Base.metadata.create_all(bind=engine)
exercise.Base.metadata.create_all(bind=engine)

app = FastAPI(title="JavaMentor API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",# Frontend React
                   "https://javamentor-frontend.vercel.app"],  # Frontend vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(exercises.router, prefix="/api/exercises", tags=["exercises"])

@app.get("/")
def root():
    return {"message": "JavaMentor API is running!"}