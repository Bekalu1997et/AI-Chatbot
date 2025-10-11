import shutil

from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
from backend.app.db import Base, engine, SessionLocal
from . import models_schemas
from . import services

Base.metadata.create_all(bind=engine)

app = FastAPI()

retriever_cache = {} # store per-user retrievers

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Backend is live"}

@app.post("/chat", response_model=models_schemas.ChatResponse)
def chat(request: models_schemas.ChatRequest, db: Session = Depends(get_db)):
    # Save user message
    services.save_message(db, request.user_id, "user", request.message)

    # Retrieve chat history
    history = services.get_chat_history(db, request.user_id)

    # 🔥 NEW: Check if user wants web search
    use_web = getattr(request, "use_web", True)

    # Generate AI response
    retriever = retriever_cache.get(request.user_id, None)
    ai_response = services.generate_response(history, retriever, use_web = use_web)

    # Save AI response
    services.save_message(db, request.user_id, "assistant", ai_response)

    return models_schemas.ChatResponse(response=ai_response)

@app.post("/chat/upload_pdf")
def upload_pdf(user_id: str, file:UploadFile = File(...)):
    file_path = f"upload_{user_id}.pdf"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    retriever = services.process_pdf(file_path)
    retriever_cache[user_id] = retriever

    return {"message": "PDF uploaded and processed successfully"}



