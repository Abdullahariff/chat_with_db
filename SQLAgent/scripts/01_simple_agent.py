"""
Simple SQL Agent Demo

This script demonstrates the basic usage of LangChain's SQL agent capabilities.
It creates a simple agent that can execute SQL queries against a SQLite database
without any safety restrictions.

Key Components:
- ChatOpenAI: The language model that powers the agent
- SQLDatabase: Wrapper for database connection and operations
- SQLDatabaseToolkit: Pre-built tools for SQL operations
- create_sql_agent: Factory function to create a SQL-capable agent

Safety Note: This agent has NO restrictions and can execute any SQL including
DELETE, DROP, INSERT, etc. It's meant for demonstration purposes only.
"""

from langchain_google_genai import ChatGoogleGenerativeAI  # Gemini chat model integration
from langchain_community.utilities import SQLDatabase  # Database connection wrapper
from langchain.agents.agent_toolkits import SQLDatabaseToolkit, create_sql_agent  # SQL agent tools
from dotenv import load_dotenv; load_dotenv()  # Load environment variables from .env file

llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

# Create Database Connection
# SQLDatabase.from_uri: Creates a database wrapper from a connection string
# Parameters:
#   - uri: SQLite database file path (creates file if it doesn't exist)
# Returns: SQLDatabase object that handles connection management and query execution
db = SQLDatabase.from_uri("sqlite:///SQLAgent/sql_agent_class.db")

agent = create_sql_agent(
    llm=llm,
    toolkit=SQLDatabaseToolkit(db=db, llm=llm),
    agent_type="tool-calling",
    verbose=True
)

# Execute a Sample Query
# agent.invoke: Executes the agent with a natural language input
# Parameters:
#   - input dict: Contains the natural language request
# Returns: Dict with "output" key containing the agent's response
# Process:
#   1. Agent analyzes the natural language request
#   2. Determines what SQL query to execute
#   3. Executes the query against the database
#   4. Formats and returns the results in natural language
print(agent.invoke({"input": "Delete first 5 customers with their regions."})["output"])