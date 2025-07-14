# Personal Assistant Agent with OpenAI Agents SDK

A simple but powerful personal assistant built using OpenAI's Agents SDK, featuring web search capabilities and optional MCP (Model Context Protocol) tools for file operations.

## Features

- **Web Search**: Search the internet for current information
- **Time & Timezone**: Get current time in any timezone
- **Calculator**: Perform mathematical calculations
- **Reminders**: Create task reminders (demo functionality)
- **Weather**: Get weather information (demo functionality)
- **File Operations**: Read/write files using MCP server (optional)

## Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Node.js and npm (optional, for MCP file operations)

## Installation

1. Clone or download this project:
```bash
mkdir personal_assistant
cd personal_assistant
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set your OpenAI API key:
```bash
export OPENAI_API_KEY=your-api-key-here
```

## Optional: Enable MCP File Operations

To enable file operations through MCP:

1. Install the MCP filesystem server:
```bash
npm install -g @modelcontextprotocol/server-filesystem
```

2. Uncomment the MCP server section in `main.py` (lines 67-85)

3. The assistant will create a `~/personal_assistant_files` directory for safe file operations

## Usage

### Interactive Mode

Run the assistant in interactive mode (chat interface):
```bash
python main.py
```

Example interactions:
- "What's the current time in Tokyo?"
- "Search for the latest news about AI"
- "Calculate 15% tip on $85.50"
- "What's the weather in Paris?" (demo)
- "Remind me to call mom tomorrow at 3pm" (demo)

### Single Query Mode

Run a single query from the command line:
```bash
python main.py "What's the weather in New York?"
```

## Available Tools

### Web Search
```
User: Search for the best Python IDE in 2024
Assistant: *searches the web and provides current recommendations*
```

### Time and Timezone
```
User: What time is it in London and Tokyo?
Assistant: *provides current times in both timezones*
```

### Calculator
```
User: Calculate (150 * 0.2) + 45
Assistant: (150 * 0.2) + 45 = 75.0
```

### Reminders (Demo)
```
User: Remind me to submit the report by 5pm
Assistant: ✅ Reminder created: 'submit the report' scheduled for by 5pm
```

### Weather (Demo)
```
User: What's the weather in San Francisco?
Assistant: Weather in San Francisco: sunny, 22°C
```

## Customization

### Change the Model

Edit line 121 in `main.py`:
```python
model="gpt-4o-mini",  # Options: "gpt-4o", "gpt-3.5-turbo", etc.
```

### Add Custom Tools

Add new function tools using the `@function_tool` decorator:
```python
@function_tool
def my_custom_tool(param: str) -> str:
    """Description of what this tool does."""
    return f"Result for {param}"
```

Then add it to the agent's tools list.

### Modify Assistant Behavior

Edit the instructions in the Agent initialization (lines 99-111) to change the assistant's personality or capabilities.

## Architecture

The personal assistant is built using:

- **OpenAI Agents SDK**: Core framework for agent orchestration
- **WebSearchTool**: Built-in tool for web searches
- **Function Tools**: Custom Python functions exposed as tools
- **MCP Servers**: Optional integration for advanced file operations

## Troubleshooting

### "OPENAI_API_KEY not set"
Make sure to export your OpenAI API key:
```bash
export OPENAI_API_KEY=sk-...
```

### MCP Server Issues
- Ensure Node.js and npm are installed
- Install the MCP server globally: `npm install -g @modelcontextprotocol/server-filesystem`
- Check that the MCP server code is uncommented in `main.py`

### Web Search Not Available
Web search is only available in certain regions. If unavailable, the assistant will inform you.

## Security Notes

- The MCP filesystem server is configured to only allow operations in `~/personal_assistant_files`
- Only safe file operations (read, write, list) are enabled
- The calculator uses restricted eval() for safety

## Next Steps

- Integrate with real calendar APIs for actual reminder functionality
- Connect to a weather API for live weather data
- Add more MCP servers for additional capabilities
- Implement conversation memory/history
- Add voice input/output capabilities

## License

This is a demo project for educational purposes. Feel free to modify and extend!