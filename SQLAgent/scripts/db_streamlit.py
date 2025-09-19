import streamlit as st
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
import pandas as pd
import matplotlib.pyplot as plt

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
    st.title("Gemini SQL Agent - Interactive Dashboard")
    st.write("Type your database question below. Results will be shown as tables and graphs if possible.")
    agent = build_agent()
    user_input = st.text_input("Enter your database question:")
    if user_input:
        response = agent.invoke({"input": user_input})
        output = response["output"]
        if isinstance(output, dict):
            cols = output.get("columns", [])
            rows = output.get("rows", [])
            if rows and cols:
                df = pd.DataFrame(rows, columns=cols)
                st.subheader("Results Table")
                st.dataframe(df)
                # Try to plot if possible
                if len(cols) >= 2 and df.shape[0] > 0:
                    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                    if numeric_cols:
                        st.subheader("Bar Chart (first numeric column)")
                        st.bar_chart(df[numeric_cols[0]])
                    if len(numeric_cols) >= 2:
                        st.subheader("Scatter Plot (first two numeric columns)")
                        st.scatter_chart(df[numeric_cols[:2]])
            else:
                st.write("No results found.")
        else:
            st.write(output)

if __name__ == "__main__":
    main()
