#!/usr/bin/env node
/**
 * Personal Assistant Agent with Web Search and Custom Tools
 *
 * This example demonstrates how to build a personal assistant using OpenAI's Agents SDK
 * with web search capabilities and custom tools for various operations.
 */

import { Agent, run, tool } from '@openai/agents';
import { z } from 'zod';
import { createReadline } from './utils/readline.js';
import process from 'process';

// Custom function tools for personal assistant capabilities

const getCurrentTime = tool({
  name: 'get_current_time',
  description: 'Get the current time in a specific timezone',
  parameters: z.object({
    timezone: z.string().default('UTC').describe('The timezone name (e.g., "America/New_York", "Europe/London", "Asia/Tokyo")')
  }),
  execute: async (input) => {
    try {
      const now = new Date();
      const formatter = new Intl.DateTimeFormat('en-US', {
        timeZone: input.timezone,
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZoneName: 'short'
      });
      
      return `Current time in ${input.timezone}: ${formatter.format(now)}`;
    } catch (error) {
      return `Unknown timezone: ${input.timezone}. Please use a valid timezone name.`;
    }
  }
});

const calculate = tool({
  name: 'calculate',
  description: 'Perform basic mathematical calculations',
  parameters: z.object({
    expression: z.string().describe('A mathematical expression to evaluate (e.g., "2 + 2", "10 * 5")')
  }),
  execute: async (input) => {
    try {
      // Use Function constructor for safer evaluation
      const sanitized = input.expression.replace(/[^0-9+\-*/().\s]/g, '');
      const result = Function(`"use strict"; return (${sanitized})`)();
      return `${input.expression} = ${result}`;
    } catch (error) {
      return `Error calculating expression: ${error.message}`;
    }
  }
});

const createReminder = tool({
  name: 'create_reminder',
  description: 'Create a reminder for a specific task (demo - doesn\'t actually set reminders)',
  parameters: z.object({
    task: z.string().describe('The task or reminder description'),
    time: z.string().describe('When to be reminded (e.g., "in 30 minutes", "tomorrow at 2pm")')
  }),
  execute: async (input) => {
    // This is a demo function - in a real implementation, you would integrate
    // with a calendar API or reminder service
    return `✅ Reminder created: '${input.task}' scheduled for ${input.time}`;
  }
});

const getWeatherInfo = tool({
  name: 'get_weather_info',
  description: 'Get weather information for a city (demo function)',
  parameters: z.object({
    city: z.string().describe('The city name')
  }),
  execute: async (input) => {
    // This is a demo function - in a real implementation, you would call
    // a weather API like OpenWeatherMap
    const weatherConditions = ['sunny', 'partly cloudy', 'cloudy', 'rainy', 'stormy'];
    const temp = Math.floor(Math.random() * 16) + 15; // 15-30°C
    const condition = weatherConditions[Math.floor(Math.random() * weatherConditions.length)];
    return `Weather in ${input.city}: ${condition}, ${temp}°C`;
  }
});

const webSearch = tool({
  name: 'web_search',
  description: 'Search the web for current information',
  parameters: z.object({
    query: z.string().describe('The search query')
  }),
  execute: async (input) => {
    // This is a demo function - in a real implementation, you would integrate
    // with a search API like Google Search API, Bing Search API, or similar
    return `🔍 Web search results for "${input.query}":\n\nThis is a demo search function. In a real implementation, this would return actual search results from a search engine API.`;
  }
});

async function createPersonalAssistant() {
  /**
   * Create and configure the personal assistant agent.
   */
  
  const agent = new Agent({
    name: 'Personal Assistant',
    instructions: `You are a helpful personal assistant with access to various tools.
        
Your capabilities include:
- Web search for finding current information
- Time and timezone queries
- Basic calculations
- Creating reminders (demo)
- Weather information (demo)

Be proactive in using your tools to provide accurate and helpful information.
When users ask questions that require current data, use web search.
Always be concise but thorough in your responses.`,
    tools: [
      webSearch,
      getCurrentTime,
      calculate,
      createReminder,
      getWeatherInfo,
    ],
    model: 'gpt-4o',
  });
  
  return agent;
}

async function runSingleQuery(agent, query) {
  /**
   * Run a single query with the assistant.
   */
  console.log(`\n🤔 You: ${query}`);
  console.log('💭 Assistant is thinking...\n');
  
  const result = await run(agent, query);
  console.log(`🤖 Assistant: ${result.finalOutput}\n`);
}

async function runInteractiveMode(agent) {
  /**
   * Run the assistant in interactive mode.
   */
  console.log('\n🎉 Personal Assistant Ready!');
  console.log('Type \'quit\' or \'exit\' to stop, or press Ctrl+C\n');
  
  const readline = createReadline();
  
  while (true) {
    try {
      const input = await readline.question('🤔 You: ');
      
      if (input.toLowerCase() === 'quit' || input.toLowerCase() === 'exit') {
        break;
      }
      
      if (input.trim() === '') {
        continue;
      }
      
      console.log('💭 Assistant is thinking...\n');
      const result = await run(agent, input);
      console.log(`🤖 Assistant: ${result.finalOutput}\n`);
      
    } catch (error) {
      console.error('❌ Error:', error.message);
    }
  }
  
  readline.close();
}

async function main() {
  /**
   * Main entry point.
   */
  console.log('🚀 Initializing Personal Assistant...');
  
  // Create the assistant
  const agent = await createPersonalAssistant();
  
  // Check if we have a command line argument for a single query
  if (process.argv.length > 2) {
    const query = process.argv.slice(2).join(' ');
    await runSingleQuery(agent, query);
  } else {
    // Run in interactive mode
    await runInteractiveMode(agent);
  }
}

// Main execution
if (!process.env.OPENAI_API_KEY) {
  console.error('❌ Error: OPENAI_API_KEY environment variable not set');
  console.error('Please set it with: export OPENAI_API_KEY=your-api-key');
  process.exit(1);
}

try {
  await main();
} catch (error) {
  if (error.name === 'InterruptedError') {
    console.log('\n\n👋 Goodbye!');
  } else {
    console.error(`\n❌ Error: ${error.message}`);
  }
  process.exit(1);
}

// Handle Ctrl+C gracefully
process.on('SIGINT', () => {
  console.log('\n\n👋 Goodbye!');
  process.exit(0);
});