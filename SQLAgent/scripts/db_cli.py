from dotenv import load_dotenv; load_dotenv()
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain.schema import SystemMessage
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from langchain_community.utilities import SQLDatabase
import sqlalchemy

# Database config
DB_URL = "sqlite:///SQLAgent/sql_agent_class.db"
engine = sqlalchemy.create_engine(DB_URL)

def get_schema():
    db = SQLDatabase.from_uri(DB_URL, include_tables=["customers","orders","order_items","products","refunds","payments"])
    return db.get_table_info()

class QueryInput(BaseModel):
    sql: str = Field(description="A single read-only SELECT statement, bounded with LIMIT when returning many rows.")

class SafeSQLTool(BaseTool):
    name: str = "execute_sql"
    description: str = "Execute exactly one SELECT statement; DML/DDL is forbidden."
    args_schema: Type[BaseModel] = QueryInput
    def _run(self, sql: str) -> str | dict:
        s = sql.strip().rstrip(";")
        if re.search(r"\b(INSERT|UPDATE|DELETE|DROP|TRUNCATE|ALTER|CREATE|REPLACE)\b", s, re.I):
            return "ERROR: write operations are not allowed."
        if ";" in s:
            return "ERROR: multiple statements are not allowed."
        if not re.match(r"(?is)^\s*select\b", s):
            return "ERROR: only SELECT statements are allowed."
        if not re.search(r"\blimit\s+\d+\b", s, re.I) and not re.search(r"\bcount\(|\bgroup\s+by\b|\bsum\(|\bavg\(|\bmax\(|\bmin\(", s, re.I):
            s += " LIMIT 200"
        try:
            with engine.connect() as conn:
                result = conn.exec_driver_sql(s)
                rows = result.fetchall()
                cols = list(result.keys()) if result.keys() else []
                return {"columns": cols, "rows": [list(r) for r in rows]}
        except Exception as e:
            return f"ERROR: {e}"
    def _arun(self, *args, **kwargs):
        raise NotImplementedError

def build_agent():
    schema_context = get_schema()
    system = f"You are a careful analytics engineer for SQLite. Use only these tables.\n\n{schema_context}"
    llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0)
    safe_tool = SafeSQLTool()
    agent = initialize_agent(
        tools=[safe_tool],
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=False,
        agent_kwargs={"system_message": SystemMessage(content=system)}
    )
    return agent

def main():
    print("Gemini SQL Agent CLI. Type your database question and press Enter. Type 'exit' to quit.")
    agent = build_agent()
    while True:
        user_input = input("\n> ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        try:
            response = agent.invoke({"input": user_input})
            if isinstance(response["output"], dict):
                cols = response["output"].get("columns", [])
                rows = response["output"].get("rows", [])
                print("Columns:", cols)
                for row in rows:
                    print(row)
            else:
                print(response["output"])
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
