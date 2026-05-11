<div align="center">
  <h1>🌌 Omni-Agent OS (formerly AI-Dispatcher)</h1>
  <p><b>A visual operating system and master orchestrator for autonomous AI development.</b></p>
  <p>
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
    <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  </p>
</div>

## 📌 Mega Description
**Omni-Agent OS** is not just a Kanban board; it is a complete, local-first **Agentic Mesh Framework**. It bridges the gap between chaotic LLM prompts and strict software engineering pipelines. 

By acting as a visual dispatcher, it clones your main repository into isolated `git worktrees`, assembles surgical context using local RAG, and spawns AI agents to write code. Before any code is pushed, a local Gatekeeper model scans the diffs for security leaks and architectural flaws. You act as the Product Owner — you drop tasks into "In Progress", and the Omni-Agent OS does the rest, streaming its thoughts and terminal commands directly to your UI.

---

## 🤖 The Omni-Agent Mesh (Absorbed Systems)

This project is the culmination of three standalone AI systems merged into one unstoppable engine:

### 1. The Knowledge Agent (RAG Librarian)
*Absorbed from `knowledge-agent`.*
Instead of feeding an entire codebase to an LLM (wasting tokens and causing hallucinations), the Knowledge Agent intercepts the task first. It connects to a local Vector DB, semantically searches your codebase and internal wikis, and injects **only the highly relevant files** into the Developer Agent's context.

### 2. The Aegis Gatekeeper (Security & QA)
*Absorbed from `local-security-agent`.*
A lightweight, offline-first security module. When the Developer Agent finishes writing code, the Gatekeeper wakes up. It scans the `git diff` for:
- Hardcoded API keys or passwords.
- Missing test coverage.
- Violations of the Antigravity architecture.
If it fails, the task is automatically rejected and sent back to "In Progress".

### 3. The Antigravity Context Builder (Rules Engine)
*Absorbed from `architecture-enforcer` and `antigravity-bar`.*
Agents do not have free will. The Context Builder parses the `~/.gemini/antigravity/` ecosystem directory, reading your personal `RULES.md` and specific workflows (e.g., `feature-pipeline.md`). It forces the LLM to follow your exact "Premium Standard" development steps.

---

## 🏗 System Architecture

Omni-Agent OS uses a **Web App + Local API** topology to ensure maximum speed, privacy, and system-level access.

- **Frontend (React + Vite + TypeScript):** A premium, glassmorphism-styled Kanban UI. Features a **Live Activity Feed** (Terminal) powered by Server-Sent Events (SSE) to watch the agents "think" in real-time, plus Token Dashboards and Project Health metrics.
- **Backend (Python FastAPI):** The orchestration heart. It manages the SQLite database, exposes REST endpoints, and runs the asynchronous `agent_runner`.
- **Git Worktree Engine:** The ultimate safety net. When a task starts, FastAPI executes `git worktree add`. The agent writes code in an isolated, temporary folder. Your `main` branch is 100% protected from AI mistakes. If the agent fails catastrophically, the system triggers an **Auto-Rollback**, destroying the worktree.

---

## 🚀 Getting Started

### 1. Start the Orchestration Backend
```bash
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Start the Dispatcher UI
```bash
cd web
npm install
npm run dev
```
Navigate to `http://localhost:5173` to access the Control Panel.

---

## 📋 GitHub Setup (For Publishing)

**Repository Name:** `Omni-Agent-OS`
**Description:** A local-first visual operating system for autonomous AI development. Features Git Worktree isolation, RAG context injection, and offline security scanning.
**Tags:** `ai-agents`, `multi-agent-system`, `fastapi`, `react`, `kanban`, `rag`, `git-worktree`, `local-first`, `autonomous-coding`
