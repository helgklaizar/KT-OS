<div align="center">
  <h1>🧠 Cognitive Agentic Router</h1>
  <p><strong>Enterprise-grade Multi-Agent System integrating Local LLMs, Vector RAG, and Text-to-SQL.</strong></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/PyTorch-Embeddings-EE4C2C.svg?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch">
    <img src="https://img.shields.io/badge/LangChain-Agents-1C3C3C.svg?style=for-the-badge" alt="LangChain">
    <img src="https://img.shields.io/badge/ChromaDB-Vector_DB-FF9900.svg?style=for-the-badge" alt="ChromaDB">
    <img src="https://img.shields.io/badge/FastAPI-REST_API-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  </p>
</div>

---

> 🍏 **Part of the Mac AI Ecosystem Initiative**
> Этот проект является частью масштабной инициативы по созданию передовых AI-инструментов для локальной работы на Apple Silicon (MLX/MPS).

## 📋 TL;DR
This project demonstrates an **Enterprise Agentic Architecture**. Instead of hardcoding AI workflows, it features an AI Supervisor (Zero-Shot ReAct Agent) that dynamically decides whether to query a **Vector Database** (for unstructured PDF/MD rules) or a **SQL Database** (for structured tabular data) using a Local HuggingFace LLM (TinyLlama/Mistral).

## 🌟 Features
- **🕵️‍♂️ Intelligent Agent Router:** Automatically chooses between RAG and SQL tools based on the user's intent.
- **📚 Local RAG Pipeline:** Uses PyTorch (`sentence-transformers`) for semantic embeddings and `ChromaDB` for vector retrieval. Bypasses bloated framework wrappers for raw Python performance.
- **📊 Text-to-SQL Analytics:** Converts natural language (e.g., "How many employees are in Sales?") into valid SQLite queries and executes them.
- **🏗 Enterprise Architecture:** Strictly follows SOLID principles, using Dependency Injection and Abstraction layers (`ILLMProvider`, `IVectorDB`).
- **🛡 E2E Integration Testing:** Includes Pytest fixtures that spin up the *real* Vector DB and execute *real* LLM inference on the CPU/MPS.

## 🚀 Quick Start
```bash
# 1. Clone the repo
git clone https://github.com/helgklaizar/cognitive-agentic-router.git
cd cognitive-agentic-router

# 2. Setup Virtual Environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Generate Fake Enterprise Data (SQL + Policies)
python src/data/generate_fake_db.py

# 4. Start the Agent REST API
python src/api/main.py
```

## 📐 Architecture & Patterns
- **Interfaces (`src/core/interfaces.py`):** The business logic is completely decoupled from the specific LLM or Vector DB.
- **RAG Use Case (`src/use_cases/rag_use_case.py`):** A custom, robust RAG chain that manually retrieves, formats, and generates text without relying on brittle framework chains.
- **Multi-Agent Router (`src/use_cases/agent_router.py`):** The LangChain Supervisor that handles the reasoning loop.

## 🤝 About Us
Developed as part of the **Chief AI Officer (CAIO) Qualification Track**. Focused on delivering privacy-first, local AI solutions without relying on paid cloud APIs. We build resilient architectures that run on local silicon.
