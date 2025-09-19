# Simple Agent CLI

This project demonstrates a simple agent using LangChain's agent framework. The agent is capable of conversational AI and can be tested through a command-line interface (CLI).

## Project Structure

```
simple-agent-cli
├── src
│   ├── 00_simple_llm.py       # Implementation of the simple agent
│   └── cli.py                 # Command-line interface for testing the agent
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Installation

To set up the project, follow these steps:

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd simple-agent-cli
   ```

2. **Create a virtual environment** (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add your API keys:
   ```
   GEMINI_API_KEY=<your_api_key>
   ```

## Usage

To run the command-line interface and interact with the agent, execute the following command:

```
python src/cli.py
```

Once the CLI is running, you can enter your questions, and the agent will respond accordingly.

## Examples

- **Question**: What is an AI agent and how does it differ from a chatbot?
- **Response**: An AI agent is a system that can autonomously perform tasks and make decisions, while a chatbot is typically designed for specific interactions and may not have autonomous capabilities.

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements for the project.

## License

This project is licensed under the MIT License. See the LICENSE file for details.