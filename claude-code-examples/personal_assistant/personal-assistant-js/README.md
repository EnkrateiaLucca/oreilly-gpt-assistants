# Personal Assistant (JavaScript)

A personal assistant built with the OpenAI Agents SDK for JavaScript. This agent provides various capabilities including web search, time queries, calculations, and more.

## Features

- ⏰ **Time & Timezone Queries**: Get current time in any timezone
- 🔍 **Web Search**: Search for current information (demo function)
- 🧮 **Calculations**: Perform basic mathematical operations
- 📝 **Reminders**: Create reminders (demo function)
- 🌤️ **Weather**: Get weather information (demo function)
- 💬 **Interactive Chat**: Chat with the assistant in real-time

## Prerequisites

- Node.js 18+ 
- OpenAI API key

## Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your-api-key-here
   ```

## Usage

### Interactive Mode

Start the assistant in interactive mode:

```bash
npm start
```

This will start an interactive chat session where you can ask questions and get responses.

### Single Query Mode

Run a single query:

```bash
npm start "What's the current time in Tokyo?"
```

### Development Mode

Run in development mode with auto-reload:

```bash
npm run dev
```

## Example Queries

- "What's the current time in New York?"
- "Calculate 15 * 24 + 100"
- "Create a reminder to call mom tomorrow at 3pm"
- "What's the weather like in Paris?"
- "Search for the latest news about AI"

## Project Structure

```
personal-assistant-js/
├── index.js           # Main application entry point
├── utils/
│   └── readline.js    # Readline utility for interactive mode
├── package.json       # Package configuration
└── README.md         # This file
```

## Tools Available

### Built-in Tools

- `get_current_time` - Get current time in any timezone
- `calculate` - Perform mathematical calculations
- `create_reminder` - Create reminders (demo)
- `get_weather_info` - Get weather information (demo)
- `web_search` - Search the web (demo)

### Extending the Assistant

To add new tools, create a new tool using the `tool()` function:

```javascript
import { tool } from '@openai/agents';
import { z } from 'zod';

const myTool = tool({
  name: 'my_tool',
  description: 'Description of what this tool does',
  parameters: z.object({
    param: z.string().describe('Parameter description')
  }),
  execute: async (input) => {
    // Your tool implementation here
    return `Result: ${input.param}`;
  }
});
```

Then add it to the agent's tools array in `index.js`.

## Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required)

## Notes

- Some tools (weather, web search) are demo functions that return mock data
- To implement real functionality, integrate with actual APIs:
  - Weather: OpenWeatherMap API, WeatherAPI, etc.
  - Web Search: Google Search API, Bing Search API, etc.
  - Reminders: Calendar APIs, notification services, etc.

## License

ISC