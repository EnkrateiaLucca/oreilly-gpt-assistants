#!/usr/bin/env python3
"""
Example usage of the Personal Assistant Agent

This script demonstrates various capabilities of the personal assistant.
"""

import asyncio
import os
from main import create_personal_assistant, Runner

async def run_examples():
    """Run example queries to demonstrate the assistant's capabilities."""
    
    # Create the assistant
    agent = await create_personal_assistant()
    
    # Example queries
    examples = [
        "What's the current time in New York, London, and Tokyo?",
        "Calculate the compound interest on $10,000 at 5% annual rate for 3 years",
        "Search for the latest developments in AI agents and autonomous systems",
        "What's 15% tip on a $127.50 restaurant bill?",
        "Create a reminder to review the quarterly report tomorrow at 2pm",
        "What's the weather forecast for Seattle?",
        "Search for healthy breakfast recipes that take less than 15 minutes",
    ]
    
    print("🎯 Personal Assistant Examples\n")
    print("=" * 60)
    
    for i, query in enumerate(examples, 1):
        print(f"\n📌 Example {i}:")
        print(f"User: {query}")
        print("\nAssistant: ", end="", flush=True)
        
        # Run the query
        result = await Runner.run(agent, query)
        print(result.final_output)
        
        print("\n" + "-" * 60)
        
        # Small delay between examples
        if i < len(examples):
            await asyncio.sleep(1)
    
    print("\n✅ Examples completed!")

async def main():
    """Main entry point."""
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please set it with: export OPENAI_API_KEY=your-api-key")
        return
    
    await run_examples()

if __name__ == "__main__":
    asyncio.run(main())