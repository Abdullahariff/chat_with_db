from dotenv import load_dotenv; load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain.schema import SystemMessage
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class DummyInput(BaseModel):
    query: str = Field(description="Any input - this tool does nothing")

class DummyTool(BaseTool):
    name: str = "dummy_tool"
    description: str = "A dummy tool that does nothing - used only for agent framework demo"
    args_schema: Type[BaseModel] = DummyInput
    def _run(self, query: str) -> str:
        return "This is a dummy tool that does nothing. I can only provide information through conversation."
    def _arun(self, *args, **kwargs):
        raise NotImplementedError

def build_agent():
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash",
        temperature=0
    )
    system_message = SystemMessage(
        content="""You are a helpful AI assistant specializing in explaining technology concepts.\nYou provide clear, concise explanations and are always friendly and professional.\nYou have access to one dummy tool, but you should prefer to answer questions directly through conversation."""
    )
    dummy_tool = DummyTool()
    agent = initialize_agent(
        tools=[dummy_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
        agent_kwargs={
            "system_message": system_message
        }
    )
    return agent

def main():
    print("Gemini Agent CLI. Type your question and press Enter. Type 'exit' to quit.")
    agent = build_agent()
    while True:
        user_input = input("\n> ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        try:
            response = agent.invoke({"input": user_input})
            print(f"Agent: {response['output']}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
import sys
from dotenv import load_dotenv; load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain.schema import SystemMessage
from typing import Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool

class DummyInput(BaseModel):
    query: str = Field(description="Any input - this tool does nothing")

class DummyTool(BaseTool):
    name: str = "dummy_tool"
    description: str = "A dummy tool that does nothing - used only for agent framework demo"
    args_schema: Type[BaseModel] = DummyInput
    def _run(self, query: str) -> str:
        return "This is a dummy tool that does nothing. I can only provide information through conversation."
    def _arun(self, *args, **kwargs):
        raise NotImplementedError

def build_agent():
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
    system_message = SystemMessage(
        content="""You are a helpful AI assistant specializing in explaining technology concepts.\nYou provide clear, concise explanations and are always friendly and professional.\nYou have access to one dummy tool, but you should prefer to answer questions directly through conversation."""
    )
    dummy_tool = DummyTool()
    agent = initialize_agent(
        tools=[dummy_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
        agent_kwargs={"system_message": system_message}
    )
    return agent

def main():
    agent = build_agent()
    print("Gemini CLI Agent. Type your question and press Enter. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        try:
            response = agent.invoke({"input": user_input})
            print(f"Agent: {response['output']}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
