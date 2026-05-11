# Архитектура проекта

## Стек технологий
- **Frontend**: React, Vite, TypeScript.
- **Styling**: Vanilla CSS / CSS Modules (Строгий дизайн-код, Glassmorphism).
- **Backend (Future)**: Python FastAPI / Node.js для запуска агентов.
- **State**: Локальное состояние (React Context / Zustand) + IndexedDB/Local JSON для хранения карточек.

## Топология (Web App + Local API)
1. **Фронтенд** отрисовывает карточки, статусы и колонки.
2. При перетаскивании карточки в `In Progress`, фронтенд (в будущем) отправит HTTP POST на локальный бекенд `http://localhost:8000/api/agents/execute`.
3. Локальный бекенд запустит скрипт агента и по SSE (Server-Sent Events) будет стримить статусы обратно на фронтенд.
