#!/usr/bin/env python3
"""
Personal Assistant Agent with Web Search and MCP Tools

This example demonstrates how to build a personal assistant using OpenAI's Agents SDK
with web search capabilities and MCP (Model Context Protocol) tools for file operations.
"""

import asyncio
import os
from datetime import datetime
import pytz
from agents import Agent, Runner, function_tool, WebSearchTool, run_demo_loop
from agents.mcp import MCPServerStdio, create_static_tool_filter
import json

# Custom function tools for personal assistant capabilities

@function_tool
def get_current_time(timezone: str = "UTC") -> str:
    """Get the current time in a specific timezone.
    
    Args:
        timezone: The timezone name (e.g., "America/New_York", "Europe/London", "Asia/Tokyo")
    """
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
        return f"Current time in {timezone}: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    except pytz.exceptions.UnknownTimeZoneError:
        return f"Unknown timezone: {timezone}. Please use a valid timezone name."

@function_tool
def calculate(expression: str) -> str:
    """Perform basic mathematical calculations.
    
    Args:
        expression: A mathematical expression to evaluate (e.g., "2 + 2", "10 * 5")
    """
    try:
        # Use eval safely for basic math operations
        allowed_names = {
            "abs": abs, "round": round, "min": min, "max": max,
            "pow": pow, "sum": sum, "len": len
        }
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error calculating expression: {str(e)}"

@function_tool
def create_reminder(task: str, time: str) -> str:
    """Create a reminder for a specific task (demo - doesn't actually set reminders).
    
    Args:
        task: The task or reminder description
        time: When to be reminded (e.g., "in 30 minutes", "tomorrow at 2pm")
    """
    # This is a demo function - in a real implementation, you would integrate
    # with a calendar API or reminder service
    return f"✅ Reminder created: '{task}' scheduled for {time}"

@function_tool
def get_weather_info(city: str) -> str:
    """Get weather information for a city (demo function).
    
    Args:
        city: The city name
    """
    # This is a demo function - in a real implementation, you would call
    # a weather API like OpenWeatherMap
    import random
    weather_conditions = ["sunny", "partly cloudy", "cloudy", "rainy", "stormy"]
    temp = random.randint(15, 30)
    condition = random.choice(weather_conditions)
    return f"Weather in {city}: {condition}, {temp}°C"

async def create_personal_assistant():
    """Create and configure the personal assistant agent."""
    
    # Initialize MCP server for file operations (optional)
    mcp_servers = []
    
    # You can enable MCP filesystem server by uncommenting below
    # Make sure to install the MCP server first:
    # npm install -g @modelcontextprotocol/server-filesystem
    """
    try:
        # Create a safe directory for file operations
        safe_dir = os.path.expanduser("~/personal_assistant_files")
        os.makedirs(safe_dir, exist_ok=True)
        
        filesystem_server = MCPServerStdio(
            params={
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", safe_dir],
            },
            tool_filter=create_static_tool_filter(
                # Only allow safe file operations
                allowed_tool_names=["read_file", "write_file", "list_directory"]
            )
        )
        mcp_servers.append(filesystem_server)
        print(f"📁 MCP filesystem server enabled for: {safe_dir}")
    except Exception as e:
        print(f"⚠️  MCP filesystem server not available: {e}")
    """
    
    # Create the personal assistant agent
    agent = Agent(
        name="Personal Assistant",
        instructions="""You are a helpful personal assistant with access to various tools.
        
Your capabilities include:
- Web search for finding current information
- Time and timezone queries
- Basic calculations
- Creating reminders (demo)
- Weather information (demo)
- File operations (if MCP server is enabled)

Be proactive in using your tools to provide accurate and helpful information.
When users ask questions that require current data, use web search.
Always be concise but thorough in your responses.""",
        tools=[
            WebSearchTool(),
            get_current_time,
            calculate,
            create_reminder,
            get_weather_info,
        ],
        mcp_servers=mcp_servers,
        model="gpt-4o",  # You can change to "gpt-4o" or other models
    )
    
    return agent

async def run_single_query(agent: Agent, query: str):
    """Run a single query with the assistant."""
    print(f"\n🤔 You: {query}")
    print("💭 Assistant is thinking...\n")
    
    result = await Runner.run(agent, query)
    print(f"🤖 Assistant: {result.final_output}\n")

async def run_interactive_mode(agent: Agent):
    """Run the assistant in interactive mode."""
    print("\n🎉 Personal Assistant Ready!")
    print("Type 'quit' or 'exit' to stop, or press Ctrl+C\n")
    
    await run_demo_loop(agent)

async def main():
    """Main entry point."""
    print("🚀 Initializing Personal Assistant...")
    
    # Create the assistant
    agent = await create_personal_assistant()
    
    # Check if we have a command line argument for a single query
    import sys
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        await run_single_query(agent, query)
    else:
        # Run in interactive mode
        await run_interactive_mode(agent)

if __name__ == "__main__":
    # Make sure OPENAI_API_KEY is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set it with: export OPENAI_API_KEY=your-api-key")
        exit(1)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")