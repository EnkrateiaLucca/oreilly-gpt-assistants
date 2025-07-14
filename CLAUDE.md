# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an O'Reilly Live Training course repository focused on building AI agents using OpenAI's GPT Assistants API. The project contains educational Jupyter notebooks demonstrating progressive concepts from basic assistant creation to advanced function calling and integrations.

## Development Commands

### Environment Setup
```bash
# Complete setup from scratch
make all

# Individual setup steps
make conda-create          # Create conda environment (gpt-assistants, Python 3.11)
make env-setup            # Setup pip-tools and ipykernel
make repo-setup           # Initialize requirements structure
make notebook-setup       # Install Jupyter kernel
make env-update           # Update dependencies using uv
make freeze               # Freeze current dependencies

# Manual setup
conda activate oreilly-gpt-assistants
pip install -r requirements/requirements.txt
```

### Testing
```bash
# Run integration tests (no automated framework)
python test_gmail_tools.py     # Test Gmail API integration
python test_calendar_tools.py  # Test Google Calendar API integration
```

### Dependency Management
```bash
# Update dependencies
uv pip compile requirements/requirements.in
make env-update
```

## Architecture Overview

### Core Components

**Notebooks Structure (Sequential Learning Path):**
- `0.0-` to `9.0-` - Main curriculum progression
- `extra-` notebooks for advanced topics
- Each notebook focuses on specific API capabilities

**Python Modules:**
- `assistants.py` - Core assistant functionality and API patterns
- `tools.py` - Tool implementations for function calling
- `app.py` - Slack bot integration
- Integration modules for Gmail, Google Calendar, GitHub

**Function Schemas:** JSON schemas in `function_schemas/` directory define API function structures for tool calling

### OpenAI Assistants API Patterns

**Standard Assistant Creation:**
```python
assistant = client.beta.assistants.create(
    name="Assistant Name",
    instructions="System instructions here...",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o"
)
```

**Thread and Message Management:**
```python
thread = client.beta.threads.create()
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="User query"
)
```

**Streaming Response Pattern:**
```python
with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    event_handler=CustomEventHandler(),
) as stream:
    stream.until_done()
```

**Function Calling Pattern:**
- Define tools in assistant creation
- Handle `requires_action` status in runs
- Use `submit_tool_outputs()` for function results

### Tool Integration Architecture

**Built-in Tools:**
- `code_interpreter` - Data analysis and visualizations
- `file_search` - Document retrieval and analysis

**Custom Function Calling:**
- Gmail API integration (read/send emails)
- Google Calendar API (CRUD operations)
- GitHub API integration
- Web scraping with BeautifulSoup4

### Environment Variables

Required for development:
```bash
OPENAI_API_KEY=your_openai_api_key

# For Google integrations
GMAIL_CLIENT_ID=your_gmail_client_id
GMAIL_CLIENT_SECRET=your_gmail_client_secret
GMAIL_REFRESH_TOKEN=your_gmail_refresh_token

# For Slack integration
SLACK_BOT_TOKEN=your_slack_bot_token
SLACK_SIGNING_SECRET=your_slack_signing_secret
```

## Code Conventions

- **Python 3.11** with conda environment management
- **Type hints** used where appropriate
- **Docstrings** for all functions
- **Error handling** with try-catch blocks around API calls
- **Singleton pattern** for Google service instances
- **Event handler classes** for streaming responses
- **4-space indentation** standard

## Testing Approach

- **Manual testing** with standalone test scripts
- **Integration tests** for external APIs (Gmail, Calendar)
- **No formal testing framework** - uses simple function-based tests with print statements
- Tests are run directly: `python test_file.py`

    ## Development Notes

    - Uses `uv` for faster dependency management
    - Jupyter notebooks are the primary development interface
    - Each notebook has corresponding documentation in `chat-assistant-files/`
    - Setup instructions provided for Gmail and Slack API integrations
    - No automated linting or CI/CD configured
    - Project structure optimized for educational progression