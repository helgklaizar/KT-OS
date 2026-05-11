class KnowledgeAgent:
    """
    Absorbed from 'knowledge-agent'.
    Connects to local RAG/VectorDB to pull context for the Developer Agent.
    """
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_context(self, task_title: str, task_desc: str) -> str:
        # TODO: Implement Qdrant/ChromaDB similarity search
        return "System Context: Project uses React + Vite. Styling: Glassmorphism."
