# search_assistant.py

## Overview

This module implements a Slack bot that integrates OpenAI Assistants with web search capabilities using Tavily API. It demonstrates how to create a conversational AI assistant that can search the web and respond to Slack messages with real-time information.

## Purpose

The bot enables:
- Real-time web search through Slack conversations
- Integration of OpenAI Assistants with external tools
- Automatic handling of tool calls and responses
- Thread-based conversation management in Slack

## Dependencies

```python
import os 
import json
import uuid 
from typing import Type
from dotenv import load_dotenv

#Slack Imports 
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

#Langchain Imports
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain.agents import AgentExecutor
from langchain_core.agents import AgentFinish
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
```

## Configuration

### Environment Variables

Required environment variables:
- `TAVILY_API_KEY`: API key for Tavily search service
- `SLACK_BOT_TOKEN`: Slack bot user OAuth token
- `SLACK_APP_TOKEN`: Slack app-level token for Socket Mode

### Initialization

```python
load_dotenv()

# Get Tavily API Key
tavily_api_key = os.getenv('TAVILY_API_KEY')

# Initialize the Slack Bolt App with the bot token
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
client = app.client
```

## Core Components

### Tavily Search Tool

```python
# Create Tavily Search Tool
search = TavilySearchAPIWrapper()
tavily_tool = TavilySearchResults(api_wrapper=search, return_direct=True, verbose=True)
```

The Tavily tool provides:
- Web search capabilities
- Direct result returns
- Verbose logging for debugging

### Assistant Management

#### create_assistant()

```python
def create_assistant(name, instructions, tools, model, as_agent):
    assistant = OpenAIAssistantRunnable.create_assistant(
        name=name,
        instructions=instructions,
        tools=tools,
        model=model,
        as_agent=as_agent
    )
    assistant_id = assistant.assistant_id
    
    return assistant_id
```

Creates a new OpenAI Assistant with specified configuration.

#### existing_assistant()

```python
def existing_assistant(assistant_id):
    agent = OpenAIAssistantRunnable(assistant_id=assistant_id, as_agent=True)
    return agent
```

Loads an existing assistant using its ID.

### Agent Execution

#### execute_agent()

```python
def execute_agent(agent, tools, input):
    tool_map = {tool.name: tool for tool in tools}
    response = agent.invoke(input)
    while not isinstance(response, AgentFinish):
        tool_outputs = []
        for action in response:
            tool_output = tool_map[action.tool].invoke(action.tool_input)
            if isinstance(tool_output, list):  # Check if the output is a list
                tool_output = json.dumps(tool_output)  # Serialize the list to a JSON string
            print(f"Tool: {action.tool}, Output Type: {type(tool_output)}, Output: {tool_output}")
            tool_outputs.append({"output": tool_output, "tool_call_id": action.tool_call_id})
        response = agent.invoke(
            {
                "tool_outputs": tool_outputs,
                "run_id": action.run_id,
                "thread_id": action.thread_id,
            }
        )
    return response
```

This function:
1. Creates a mapping of tool names to tool objects
2. Invokes the agent with the input
3. Handles tool calls in a loop until completion
4. Serializes list outputs to JSON strings
5. Submits tool outputs back to the agent
6. Returns the final response

### Slack Integration

#### Message Handler

```python
@app.message("")
def message_handler(message, say, ack):
    ack()
    print(message)
    user_query = message['text']
    from_user = message['user']
    response = execute_agent(assistant, tools, {"content": user_query})
    ai_response = response.return_values["output"]
    print(ai_response)
    say(ai_response, thread_ts=message['ts'])
```

The message handler:
- Acknowledges messages immediately
- Extracts user query from the message
- Executes the agent with the query
- Responds in the same thread

## Usage Flow

1. **Bot Initialization**:
   - Loads environment variables
   - Sets up Slack app and Tavily search tool
   - Loads the assistant

2. **Message Reception**:
   - User sends a message in Slack
   - Bot acknowledges and processes the message

3. **Search Execution**:
   - Assistant determines if search is needed
   - Calls Tavily API for web search
   - Processes search results

4. **Response Generation**:
   - Assistant formulates response based on search results
   - Bot posts response in the same thread

## Example Interactions

```python
# Example search query
search_input = {"query": "What is the Tesla stock price as of today?"}

# Example message handling
# User: "What's the current weather in New York?"
# Bot: Searches for weather information and responds with current conditions
```

## Socket Mode

The bot uses Socket Mode for real-time event handling:

```python
if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
```

Socket Mode benefits:
- No public URL required
- Real-time bidirectional communication
- Simplified development setup

## Error Handling

The implementation includes:
- Type checking for tool outputs
- JSON serialization for list outputs
- Debug logging for tool execution
- Graceful handling of API responses

## Security Considerations

- Store API keys in environment variables
- Use `.env` file for local development
- Never commit credentials to version control
- Implement rate limiting for production use

## Assistant Configuration

The code uses a pre-existing assistant:
```python
assistant_id = "asst_qPkFH6kDCiYuCXZgW259VyDb"
```

To create a new assistant, use the `create_assistant()` function with:
- Name and instructions
- Tool configurations
- Model selection (e.g., "gpt-4")
- Agent mode enabled

## Complete Code

```python
import os 
import json
import uuid 
from typing import Type
from dotenv import load_dotenv

#Slack Imports 
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

#Langchain Imports
from langchain.agents.openai_assistant import OpenAIAssistantRunnable
from langchain.agents import AgentExecutor
from langchain_core.agents import AgentFinish
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper

load_dotenv()

#Get Tavily API Key
tavily_api_key = os.getenv('TAVILY_API_KEY')


# Initialize the Slack Bolt App with the bot token
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
client = app.client

#Create Tavily Search Tool
search = TavilySearchAPIWrapper()
tavily_tool = TavilySearchResults(api_wrapper=search, return_direct=True, verbose=True)
search_input = {"query": "What is the Tesla stock price as of today?"}  
#output = tavily_tool.invoke(search_input)

# Print the output
#print("Output:", output)


#Function to create assistant
def create_assistant(name, instructions, tools, model, as_agent):
    assistant = OpenAIAssistantRunnable.create_assistant(
        name=name,
        instructions=instructions,
        tools=tools,
        model=model,
        as_agent=as_agent
    )
    assistant_id = assistant.assistant_id
    
    return assistant_id


assistant_id = "asst_qPkFH6kDCiYuCXZgW259VyDb"

#Function to use existing assistant
def existing_assistant(assistant_id):
    agent = OpenAIAssistantRunnable(assistant_id=assistant_id, as_agent=True)
    return agent

#Initialize Assistant and Tools
assistant = existing_assistant(assistant_id)
tools = [tavily_tool]

# Agent executor function for executing agents
def execute_agent(agent, tools, input):
    tool_map = {tool.name: tool for tool in tools}
    response = agent.invoke(input)
    while not isinstance(response, AgentFinish):
        tool_outputs = []
        for action in response:
            tool_output = tool_map[action.tool].invoke(action.tool_input)
            if isinstance(tool_output, list):  # Check if the output is a list
                tool_output = json.dumps(tool_output)  # Serialize the list to a JSON string
            print(f"Tool: {action.tool}, Output Type: {type(tool_output)}, Output: {tool_output}")
            tool_outputs.append({"output": tool_output, "tool_call_id": action.tool_call_id})
        response = agent.invoke(
            {
                "tool_outputs": tool_outputs,
                "run_id": action.run_id,
                "thread_id": action.thread_id,
            }
        )
    return response


# Example usage
#response = execute_agent(assistant, tools, {"content": "@<U05K6HV02UEI>: Send a message to the general channel saying hi"})
#print(response)
#print(response.return_values["output"])

# Listen and handle messages
@app.message("")
def message_handler(message, say, ack):
    ack()
    print(message)
    user_query = message['text']
    from_user = message['user']
    response = execute_agent(assistant, tools, {"content": user_query})
    ai_response = response.return_values["output"]
    print(ai_response)
    say(ai_response, thread_ts=message['ts'])


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
```