"""
Command-Line Interface for Simple Agent Application

This script provides a command-line interface (CLI) to interact with the simple agent implemented in 00_simple_llm.py. Users can enter questions and receive responses directly from the agent.

Key Features:
- Interactive prompt for user input
- Displays agent responses in the terminal
- Graceful error handling for user input

Usage:
1. Run the script from the command line.
2. Enter your questions when prompted.
3. Type 'exit' to quit the CLI.
"""

import sys
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain.schema import SystemMessage
from dotenv import load_dotenv
from dummy_tool import DummyTool  # Assuming DummyTool is in the same directory

# Load environment variables
load_dotenv()

def main():
    # Initialize the Language Model
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0
    )

    # Define System Message for Agent
    system_message = SystemMessage(
        content="""You are a helpful AI assistant specializing in explaining technology concepts.
        You provide clear, concise explanations and are always friendly and professional.
        You have access to one dummy tool, but you should prefer to answer questions directly through conversation."""
    )

    # Create Dummy Tool Instance
    dummy_tool = DummyTool()

    # Create Agent with Dummy Tool
    agent = initialize_agent(
        tools=[dummy_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        agent_kwargs={
            "system_message": system_message
        }
    )

    print("Welcome to the Simple Agent CLI! Type 'exit' to quit.")
    
    while True:
        question = input("You: ")
        if question.lower() == 'exit':
            print("Exiting the CLI. Goodbye!")
            break
        
        response = agent.invoke({"input": question})
        print(f"Agent: {response['output']}")

if __name__ == "__main__":
    main()
"""