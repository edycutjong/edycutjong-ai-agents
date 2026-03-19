import os
import pandas as pd
from sqlalchemy import create_engine, text
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
try:
    from langchain.chains import create_sql_query_chain
except ImportError:  # pragma: no cover
    from langchain_classic.chains import create_sql_query_chain  # pragma: no cover
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

try:
    from config import config
    from prompts.system_prompts import EXPLAIN_PREFIX
except ImportError:  # pragma: no cover
    # Fallback for relative imports if run as package
    from ..config import config  # pragma: no cover
    from ..prompts.system_prompts import EXPLAIN_PREFIX  # pragma: no cover

class SQLQueryBuilder:
    def __init__(self, db_uri: str = config.DEFAULT_DB_URI, api_key: str = None):
        self.db_uri = db_uri
        self.api_key = api_key or config.OPENAI_API_KEY

        if not self.api_key:
            raise ValueError("OpenAI API Key is required.")  # pragma: no cover

        self.llm = ChatOpenAI(
            model=config.MODEL_NAME,
            temperature=config.TEMPERATURE,
            api_key=self.api_key
        )
        self.db = SQLDatabase.from_uri(self.db_uri)
        self.engine = create_engine(self.db_uri)

        # Chain for generating SQL
        self.sql_chain = create_sql_query_chain(self.llm, self.db)

    def get_schema(self) -> str:
        """Returns the database schema."""
        return self.db.get_table_info()  # pragma: no cover

    def generate_query(self, question: str) -> str:
        """Generates a SQL query from a natural language question."""
        response = self.sql_chain.invoke({"question": question})
        # Clean up the response (sometimes it includes '```sql ... ```')
        cleaned_query = response.strip()
        if cleaned_query.startswith("```sql"):
            cleaned_query = cleaned_query[6:]  # pragma: no cover
        if cleaned_query.startswith("```"):
            cleaned_query = cleaned_query[3:]  # pragma: no cover
        if cleaned_query.endswith("```"):
            cleaned_query = cleaned_query[:-3]  # pragma: no cover
        return cleaned_query.strip()

    def execute_query(self, query: str) -> pd.DataFrame:
        """Executes a SQL query and returns the result as a DataFrame."""
        try:
            # Use pandas read_sql for better DataFrame handling
            with self.engine.connect() as connection:
                df = pd.read_sql(text(query), connection)
            return df
        except Exception as e:  # pragma: no cover
            raise e  # pragma: no cover

    def explain_query(self, query: str, question: str) -> str:
        """Explains the SQL query in simple terms."""
        prompt = PromptTemplate.from_template(  # pragma: no cover
            EXPLAIN_PREFIX + "\nQuery: {query}\nQuestion: {question}\nExplanation:"
        )
        chain = prompt | self.llm | StrOutputParser()  # pragma: no cover
        return chain.invoke({"query": query, "question": question})  # pragma: no cover

    def validate_query(self, query: str) -> bool:
        """Basic validation to prevent destructive queries."""
        forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE"]
        query_upper = query.upper()
        for word in forbidden:
            if word in query_upper:
                return False
        return True
