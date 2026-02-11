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

---

## 📚 OpenClaw Documentation

We've included comprehensive documentation about **OpenClaw**, a sophisticated personal AI assistant framework, to help you study advanced chatbot architecture and design patterns.

OpenClaw is an open-source project that demonstrates:
- Multi-channel messaging (WhatsApp, Telegram, Slack, Discord, etc.)
- Local-first architecture with WebSocket-based control plane
- Extensible tool and skill system
- Voice integration (Voice Wake + Talk Mode)
- Advanced session management and security

### 📖 Available Documentation

- **[Overview](./docs/openclaw/README.md)** - Introduction and quick reference
- **[Architecture](./docs/openclaw/architecture.md)** - Core architecture and design patterns
- **[Source Code Review](./docs/openclaw/source-code-review.md)** - Guide to navigating the codebase
- **[Components & Features](./docs/openclaw/components-features.md)** - Detailed feature breakdown
- **[Integration Guide](./docs/openclaw/integration-possibilities.md)** - How to apply OpenClaw concepts

### 🔗 Official OpenClaw Resources

- **Repository:** [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)
- **Website:** [openclaw.ai](https://openclaw.ai)
- **Documentation:** [docs.openclaw.ai](https://docs.openclaw.ai)
- **Discord:** [discord.gg/clawd](https://discord.gg/clawd)

These resources are perfect for learning about advanced chatbot architecture and can inspire improvements to this project!
