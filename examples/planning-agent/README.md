# Planning Agent Example

A comprehensive planning agent built with **deepagents** that analyzes requirements, researches codebases, and generates detailed development plans.

> **📝 Note**: Use `main_simple.py` (recommended, tested) instead of `main.py` (comprehensive reference implementation)

## Overview

This example demonstrates how to use deepagents to create an AI-powered planning assistant that:

1. **Fetches requirements** from Rally (or other project management tools)
2. **Researches codebases** to find relevant implementations
3. **Analyzes technical feasibility** and estimates effort
4. **Generates comprehensive plans** with phases, risks, and resource allocation
5. **Uses specialized sub-agents** for requirements analysis, research, and risk assessment

## Features

- 🎯 **Requirements Analysis**: Parses Rally epics/features and identifies gaps
- 🔍 **Code Research**: Searches codebases for relevant implementations
- ⚡ **Feasibility Assessment**: Evaluates complexity, risks, and effort
- 👥 **Resource Planning**: Considers team capacity and skills
- 📊 **Sub-Agents**: Specialized agents for requirements, research, and risk analysis
- 📝 **Document Generation**: Creates markdown planning documents
- ✅ **Todo Tracking**: Uses planning middleware to track progress

## Installation

### Prerequisites

- Python 3.11 or higher
- An API key for Anthropic (Claude) or OpenAI

### Setup

1. **Install dependencies**:

**With UV (Recommended - 10-100x faster! ⚡):**
```bash
cd examples/planning-agent
uv pip install -r requirements.txt
```

**With pip (Traditional):**
```bash
cd examples/planning-agent
pip install -r requirements.txt
```

> 💡 **Tip**: Install UV for blazingly fast package installation:
> ```bash
> curl -LsSf https://astral.sh/uv/install.sh | sh
> ```
> See [UV_GUIDE.md](UV_GUIDE.md) for more details.

2. **Set up your API key** (choose one or both):

```bash
# Option 1: Anthropic Claude (default, recommended)
export ANTHROPIC_API_KEY="your-api-key-here"

# Option 2: OpenAI GPT-4
export OPENAI_API_KEY="your-api-key-here"

# Both work! deepagents will use Claude by default if both are set
```

3. **Test the installation**:

```bash
python test_agent.py
```

## Usage

### Interactive Mode

Run the agent in interactive mode to chat with it:

```bash
python main_simple.py
```

This starts an interactive session where you can:
- Ask questions about planning
- Request plans for specific epic IDs
- Type `demo` for a demonstration
- Type `quit` to exit

Example session:
```
💬 You: Create a plan for Epic US12345
🤖 Agent working...

🤖 Agent: I'll help you create a comprehensive plan for Epic US12345.
Let me start by fetching the requirements...

[Agent analyzes requirements, researches code, assesses feasibility]

📁 Created 2 file(s):
  - planning_document_US12345.md
  - planning_summary_US12345.json
```

### Command Line Mode

Run the agent for a specific epic:

```bash
python main_simple.py US12345
```

Or with additional context:

```bash
python main_simple.py US12345 "Focus on backend services, prioritize security"
```

### LangGraph Studio

Test with LangGraph Studio for visual debugging:

```bash
langgraph dev
```

Then open [http://localhost:8123](http://localhost:8123) in your browser.

## Architecture

### Tools

The agent has access to these tools:

1. **fetch_rally_requirements**: Fetches epic/feature details from Rally
2. **search_codebase**: Searches repositories for relevant code
3. **analyze_technical_feasibility**: Evaluates complexity and risks
4. **get_team_resources**: Gets team capacity and availability

### Sub-Agents

The agent can delegate to specialized sub-agents:

1. **requirements-analyst**: Deep requirements analysis and gap identification
2. **technical-researcher**: Codebase research and pattern identification
3. **risk-analyst**: Risk identification and mitigation strategies

### Middleware

The agent uses deepagents middleware:

- **PlanningMiddleware**: Adds todo list tracking capabilities
- **FilesystemMiddleware**: Enables file creation and editing
- **SubAgentMiddleware**: Enables spawning specialized sub-agents
- **SummarizationMiddleware**: Manages conversation context

## Customization

### Add Your Own Tools

Define custom tools in `main_simple.py`:

```python
@tool
def your_custom_tool(param: str) -> str:
    """Tool description for the AI."""
    # Your implementation
    return result

# Add to agent creation
tools = [
    fetch_rally_requirements,
    search_codebase,
    your_custom_tool,  # Add here
]
```

### Modify Instructions

Update the agent's behavior by editing `PLANNING_AGENT_INSTRUCTIONS`:

```python
PLANNING_AGENT_INSTRUCTIONS = """
You are an expert planning agent...

[Your custom instructions]
"""
```

### Add Sub-Agents

Create specialized sub-agents for your workflow:

```python
CUSTOM_SUBAGENT: SubAgent = {
    "name": "custom-agent",
    "description": "What this agent does",
    "prompt": "Detailed instructions for the sub-agent"
}

# Add to subagents list
subagents = [
    REQUIREMENTS_ANALYST,
    CUSTOM_SUBAGENT,
]
```

### Connect Real APIs

Replace mock implementations with real API calls:

```python
@tool
def fetch_rally_requirements(epic_id: str) -> str:
    """Fetch from real Rally API."""
    import requests
    
    response = requests.get(
        f"https://rally1.rallydev.com/slm/webservice/v2.0/hierarchicalrequirement/{epic_id}",
        headers={"Authorization": f"Bearer {RALLY_API_KEY}"}
    )
    return response.json()
```

## Examples

### Example 1: Simple Planning Request

```python
from main_simple import run_planning_session

result = run_planning_session("US12345")
print(result["planning_document"])
```

### Example 2: Stream Planning Process

```python
agent = create_planning_agent()

for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "Plan for US12345"}]},
    stream_mode="values"
):
    print(chunk)
```

### Example 3: Access Generated Files

```python
result = run_planning_session("US12345")
files = result["files"]

# Save to disk
for filename, content in files.items():
    with open(f"output/{filename}", "w") as f:
        f.write(content)
```

## Testing

Run the test suite:

```bash
python test_agent.py
```

This will:
1. Test each tool individually
2. Test agent creation
3. Test simple invocations
4. Test full planning requests

Expected output:
```
🧪 Planning Agent Test Suite
================================================================================

Testing Individual Tools
1. Testing fetch_rally_requirements...
   ✅ fetch_rally_requirements works!
...
✅ ALL TESTS PASSED!
```

## Troubleshooting

### No API Key Error

**Error**: `anthropic.AuthenticationError: Invalid API key`

**Solution**: Ensure you've set your API key:
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### Module Not Found

**Error**: `ModuleNotFoundError: No module named 'deepagents'`

**Solution**: Install from the parent directory:
```bash
cd ../..  # Go to deepagents root
uv pip install -e .  # Fast!
# Or: pip install -e .
```

### LangGraph CLI Not Found

**Error**: `langgraph: command not found`

**Solution**: Install langgraph-cli:
```bash
uv pip install 'langgraph-cli[inmem]'  # Fast!
# Or: pip install langgraph-cli[inmem]
```

## Advanced Features

### Using Different Models

The agent uses **Claude Sonnet 4** by default. To use OpenAI or customize:

**Option 1: Use OpenAI GPT-4o**
```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o", temperature=0)

agent = create_deep_agent(
    tools=tools,
    instructions=PLANNING_AGENT_INSTRUCTIONS,
    model=model,
)
```

**Option 2: Use a different Claude model**
```python
from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model="claude-3-5-sonnet-20241022", max_tokens=8192)

agent = create_deep_agent(
    tools=tools,
    instructions=PLANNING_AGENT_INSTRUCTIONS,
    model=model,
)
```

**Option 3: Set via environment (keeps code unchanged)**
```python
# In main_simple.py, add at the top:
import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# Then in create_planning_agent():
if os.getenv("OPENAI_API_KEY"):
    model = ChatOpenAI(model="gpt-4o", temperature=0)
else:
    model = ChatAnthropic(model="claude-sonnet-4-20250514")

agent = create_deep_agent(
    tools=tools,
    instructions=PLANNING_AGENT_INSTRUCTIONS,
    model=model,
)
```

### Adding Human-in-the-Loop

Require approval for specific tools:

```python
from langchain.agents.middleware.human_in_the_loop import ToolConfig

tool_configs = {
    "fetch_rally_requirements": ToolConfig(interrupt_before=True),
}

agent = create_deep_agent(
    tools=tools,
    instructions=PLANNING_AGENT_INSTRUCTIONS,
    tool_configs=tool_configs,
)
```

### Adding Memory with Checkpointers

Persist conversation state:

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()

agent = create_deep_agent(
    tools=tools,
    instructions=PLANNING_AGENT_INSTRUCTIONS,
    checkpointer=checkpointer,
)

# Use with thread_id
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Plan for US12345"}]},
    config={"configurable": {"thread_id": "session-123"}}
)
```

## Project Structure

```
planning-agent/
├── main.py              # Original comprehensive implementation
├── main_simple.py       # Simplified, testable version
├── test_agent.py        # Test suite
├── requirements.txt     # Python dependencies
├── langgraph.json       # LangGraph configuration
└── README.md           # This file
```

## Learn More

- [deepagents Documentation](https://github.com/langchain-ai/deepagents)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Tools](https://python.langchain.com/docs/modules/tools/)

## License

MIT License - See parent project for details.
