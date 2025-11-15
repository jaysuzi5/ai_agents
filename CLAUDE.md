# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**ai-agents** is a Python project for training and testing AI agents using the LangGraph framework. It demonstrates autonomous agent development with multi-tool integration, persistent memory, and web-based interfaces for testing.

The project uses a training-first approach with Jupyter notebooks that progressively build complexity:
- `01_simple/` - Basic agent setup with tools, memory, and UI
- `02_descriptive_agent/` - More advanced agent patterns and configurations

## Development Setup and Commands

### Environment and Dependencies

**Python Version:** 3.13.2 (pinned in `.python-version`)

**Package Manager:** `uv` (fast Python package resolver)

**Install dependencies:**
```bash
uv sync
```

**Install with test dependencies:**
```bash
uv sync --all-groups
```

**Run main entry point:**
```bash
python main.py
```

### Jupyter Notebooks (Primary Development)

The project development happens primarily in Jupyter notebooks.

**Run Jupyter server:**
```bash
jupyter notebook
```

**Key notebooks:**
- `Training/LangGraph/01_simple/langgraph_agent.ipynb` - Start here for basic agent concepts
- `Training/LangGraph/02_descriptive_agent/langgraph_detailed_agents.ipynb` - Advanced patterns

### Testing

**Run all tests:**
```bash
pytest
```

**Run specific test file:**
```bash
pytest tests/test_file.py
```

**Run with coverage:**
```bash
pytest --cov
```

**Run specific test:**
```bash
pytest tests/test_file.py::test_function_name
```

**Run async tests specifically:**
```bash
pytest -k "test_" --asyncio-mode=auto
```

Note: Test infrastructure is configured but tests directory not yet created.

## Project Structure and Architecture

### Key Components

**LangGraph Framework**
- Core framework for building agent graphs as state machines
- Agents process information through nodes and edges in a directed graph
- Checkpointing enabled via SQLite for persistent execution state

**Tool Integration**
- Google Search integration (via Serper API configured in `.env`)
- Wikipedia API for knowledge retrieval
- File system operations for agent outputs
- Web scraping capabilities (BeautifulSoup, Playwright for browser automation)

**Memory System**
- SQLite-based persistent memory (`memory.db` files in sandbox directories)
- Uses `langgraph-checkpoint-sqlite` for storing graph execution state
- Enables agent memory across multiple conversations/runs

**UI and Testing**
- Gradio web interface for interactive agent testing
- Located in notebook sandbox directories for easy testing
- Provides chat-like interface for agent interaction

### Data Flow in Agents

1. **Input Processing**: User query enters the agent graph
2. **Tool Selection**: Agent decides which tools to use based on query
3. **Tool Execution**: Selected tools (Search, Wikipedia, File ops) execute
4. **Response Generation**: Agent synthesizes tool outputs into natural language response
5. **State Persistence**: Graph state saved to SQLite for recovery/continuation

### Configuration and Secrets

**Environment Variables** (in `.env`, never committed):
- Multiple LLM API keys (OpenAI, Anthropic, Google, DeepSeek, Groq, XAI)
- Tool APIs (Serper for search, HuggingFace, SendGrid)
- LangSmith credentials for tracing and monitoring
- Custom service credentials (Pushover)

**LangSmith Tracing**: Enabled by default when env vars present - tracks agent execution for debugging

### Dependencies Organization

**Core LLM & Agent Stack:**
- `langgraph` - Agent graph framework
- `langchain`, `langchain-community`, `langchain-experimental` - LLM toolkit
- `langchain-openai`, `langchain-google-genai` - Model providers
- `langgraph-checkpoint-sqlite` - Persistent state management

**Tools & Web Integration:**
- `beautiful-soup4`, `lxml` - HTML parsing
- `playwright` - Browser automation
- `wikipedia` - Knowledge retrieval
- `gradio` - Web UI

**Utilities:**
- `python-dotenv` - Environment variable loading
- `uuid7` - Unique ID generation
- `ipykernel` - Jupyter integration

**Testing** (optional group):
- `pytest`, `pytest-asyncio`, `pytest-cov`, `pytest-mock`

## Common Development Patterns

### Creating a New Agent

1. Create a new notebook in `Training/LangGraph/[name]/`
2. Import required modules: `langgraph`, `langchain`, `langgraph_checkpoint_sqlite`
3. Define tools as LangChain tools
4. Create agent graph with nodes and edges
5. Add SQLite checkpointing for persistence
6. Build Gradio interface for testing
7. Test via the Gradio UI in the notebook

### Working with Tools

Tools are defined as callables with type hints for LangChain tool wrapping. The agent uses an agentic loop to decide when to call tools based on the query and previous responses.

### Database and State

SQLite databases (`memory.db*` files) are created automatically by LangGraph's checkpoint system. These store:
- Agent execution history
- Tool call results
- Conversation state for multi-turn interactions

They can be deleted to reset agent memory; new databases are created on next run.

## Git Workflow Notes

- Repository is early-stage (single initial commit)
- No CI/CD pipeline yet
- Main branch is primary development branch
- `.gitignore` correctly excludes: `.env`, `__pycache__/`, `.venv/`, `sandbox/`, `memory.db*`, `.coverage`

## File Organization

- **Training/** - Educational notebooks and examples
- **sandbox/** - Output directories (in each notebook directory, gitignored)
- **Root configs** - `pyproject.toml`, `.env`, `.python-version`
- **Root scripts** - `main.py` (placeholder entry point)
