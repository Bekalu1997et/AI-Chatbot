# 🤖 AI Chatbot 
A lightweight, end-to-end AI chatbot featuring **web search**, **PDF upload**, and **memory persistence** — powered by **Phi-3 Mini** through **Ollama**.  
Built with **FastAPI** for the backend and **Streamlit** for the frontend. Fully containerized with **Docker** and orchestrated via **Docker Compose**.

---

## 🚀 Features
- 🧠 **Memory** – Persistent conversation context stored in SQLite  
- 🌐 **Web Search** – Retrieve up-to-date information  
- 📄 **PDF Upload** – Query content from uploaded documents  
- ⚙️ **Lightweight Model** – Runs Phi-3 Mini locally via Ollama  
- 🖥️ **Streamlit UI + FastAPI Backend** – Clean architecture with modular services  
- 🐳 **Dockerized** – One-command setup using Docker Compose  

---

## 🧱 Project Structure
```

ai-chatbot/
│
├── backend/               # FastAPI backend
│   ├── app
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/              # Streamlit frontend
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
├── README.md
└── .gitignore

````

---

## ⚙️ Quick Start

### 1. Prerequisites
- [Docker](https://www.docker.com/) installed  
- [Ollama](https://ollama.ai/) installed and running locally  

### 2. Clone and Run
```bash
git clone https://github.com/<your-username>/ai-chatbot.git
cd ai-chatbot
docker-compose up --build
````

### 3. Access

* **Frontend (Streamlit):** [http://localhost:8501](http://localhost:8501)
* **Backend (FastAPI docs):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧠 Environment Variables

Create a `.env` file (optional):

```
DB_PATH=./chat_memory.db
OLLAMA_MODEL=phi3:mini
```

---

## 🧩 Tech Stack

* **Frontend:** Streamlit
* **Backend:** FastAPI
* **Model:** Phi-3 Mini via Ollama
* **Database:** SQLite
* **Containerization:** Docker & Docker Compose
