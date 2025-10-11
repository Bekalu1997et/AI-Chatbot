from sqlalchemy.orm import Session
from backend.app import models
from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import HumanMessage
from ddgs import DDGS
#from langchain_community.tools import DuckDuckGoSearchRun
import os

# ------------------ LLM SETUP ------------------
# Use Phi-3 Mini model (CPU friendly)
llm = ChatOllama(model="phi3:mini")
local_model_path = "./local_models/all-MiniLM-L6-v2"
# Embedding model (lightweight and accurate)
embeddings = HuggingFaceEmbeddings(model_name= "sentence-transformers/all-MiniLM-L6-v2")


# Directory for vector store
VECTORSTORE_DIR = "../vectorstore"
os.makedirs(VECTORSTORE_DIR, exist_ok=True)

# ------------------ DATABASE FUNCTIONS ------------------
def save_message(db: Session, user_id: str, role: str, message: str):
    chat = models.ChatHistory(user_id=user_id, role=role, message=message)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

def get_chat_history(db: Session, user_id: str):
    return db.query(models.ChatHistory).filter(models.ChatHistory.user_id == user_id).all()
def safe_web_search(query: str):
    search = DDGS()
    try:
        return search.text(query)
    except Exception as e:
        print(f"[Web Search Error] {e}")
        return "⚠️ Web search failed. Network timeout or API issue."
# ------------------ LLM RESPONSE ------------------
def generate_response(history, retriever=None, use_web=True):
    """
    Generate a response from Phi-3 using chat history and optional PDF retriever.
    """
    if not history:
        return "Hello! How can I assist you today?"

    # Extract conversation and context
    messages = [(h.role, h.message) for h in history]
    user_query = history[-1].message if history else ""

    context = ""
# PDF retriever
    if retriever:
        docs = retriever.invoke(user_query)
        context += "\n\n".join([d.page_content for d in docs[:3]])
# Web Search
    if use_web:
        web_results = safe_web_search(user_query)
        context += f"\n web results: {web_results}"


    # Build prompt

    prompt = f"""
You are a helpful AI assistant.
Context from relevant documents:
{context}

Conversation so far:
{messages}

Reply helpfully and clearly to the latest user message.
"""

    # Invoke model
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

# ------------------ PDF PROCESSING ------------------
def process_pdf(file_path: str):
    """
    Load, split, embed, and return retriever for a given PDF file.
    """
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore.as_retriever()


