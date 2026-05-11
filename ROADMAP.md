# ROADMAP: AI-Dispatcher

## Phase 1: Dispatcher UI (Current)
- [x] Скаффолдинг React + Vite.
- [ ] Интеграция Канбан-доски с новым видением (Agent Cards).
- [ ] Создание дашбордов: Token Cost, Project Health.
- [ ] Создание панели Live Activity Feed (Терминал логов).
- [ ] Окно "Stuck Protocol" (диалог с агентом).

## Phase 2: The Core Engine (FastAPI + Git)
- Развертывание Python FastAPI бекенда.
- Интеграция SQLite для хранения задач.
- Реализация Git Worktrees Engine (Изолированные ветки под задачу).
- Скрипты Auto-Rollback.

## Phase 3: Agentic Mesh & Memory
- Подключение LLM (Claude/GPT-4o) для Developer Agent.
- Интеграция локальной MLX/Ollama для Gatekeeper Agent (Проверка кода).
- Настройка Векторной БД (Chroma) для Auto-Context Injection.
- Scout Agent для фонового анализа.
