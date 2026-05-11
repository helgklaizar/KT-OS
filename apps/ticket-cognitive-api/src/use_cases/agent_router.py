from langchain.agents import Tool, initialize_agent, AgentType
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from src.core.interfaces import ILLMProvider
from src.core.logger import get_logger
from src.use_cases.rag_use_case import SupportRAGUseCase

logger = get_logger(__name__)

class MultiAgentRouter:
    """Agentic workflow that decides whether to use RAG (Vector DB) or SQL Database."""
    
    def __init__(self, llm_provider: ILLMProvider, rag_use_case: SupportRAGUseCase, db_uri: str = "sqlite:///src/data/db/company.db"):
        self.llm_provider = llm_provider
        self.rag_use_case = rag_use_case
        self.db_uri = db_uri
        self.agent = None

    def _setup_sql_tool(self):
        """Creates a tool to query the relational database."""
        logger.info(f"Connecting to SQL Database at {self.db_uri}")
        db = SQLDatabase.from_uri(self.db_uri)
        llm = self.llm_provider.get_llm()
        
        sql_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
        
        return Tool(
            name="EmployeeDatabase",
            func=sql_chain.run,
            description="Useful for when you need to answer questions about employees, departments, or emails. Input should be a question."
        )

    def _setup_rag_tool(self):
        """Creates a tool to query the Knowledge Base."""
        return Tool(
            name="KnowledgeBase",
            func=self.rag_use_case.answer_query,
            description="Useful for when you need to answer questions about company rules, refund policies, remote work, or onboarding."
        )

    def initialize_agent(self):
        """Initializes the Agent Supervisor."""
        logger.info("Initializing Agent Supervisor...")
        sql_tool = self._setup_sql_tool()
        rag_tool = self._setup_rag_tool()
        
        tools = [sql_tool, rag_tool]
        llm = self.llm_provider.get_llm()
        
        # We use a Zero-shot ReAct agent
        self.agent = initialize_agent(
            tools, 
            llm, 
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
            verbose=True,
            handle_parsing_errors=True
        )
        logger.info("Agent Supervisor is ready to route tasks.")

    def run_query(self, query: str) -> str:
        """Executes a query through the Agent router."""
        logger.info(f"Supervisor received query: {query}")
        if not self.agent:
            self.initialize_agent()
            
        try:
            response = self.agent.run(query)
            return response
        except Exception as e:
            logger.error(f"Agent failed to process query: {str(e)}")
            return "Agent encountered an error deciding the routing path."
