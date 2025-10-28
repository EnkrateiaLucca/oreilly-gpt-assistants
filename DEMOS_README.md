# Demo Applications - OpenAI Responses API

This directory contains two demo applications showcasing the OpenAI Responses API for the O'Reilly Live Training course.

## Overview

Both demos demonstrate key features of the Responses API:
- Stateless conversation management with `previous_response_id`
- Built-in tools (File Search and Code Interpreter)
- Streaming responses for real-time output
- Simple, intuitive API design

## Demo 1: PDF Document Search

**File:** `demo_1_pdf_search.py`

### Description
A research assistant that searches through PDF documents using natural language queries. Built with the File Search tool and vector stores.

### Features
- Upload multiple PDF documents
- Natural language search across all documents
- Conversation continuity (follow-up questions)
- Source citations from documents
- Real-time streaming responses
- Automatic vector store cleanup

### Usage

```bash
# Run the demo
python demo_1_pdf_search.py
```

### Example Queries
- "What is the main topic of these papers?"
- "Explain the attention mechanism in simple terms"
- "What are the key findings about the future of agents?"

### Customization

Update the `pdf_files` list in `main()` to use your own PDFs:

```python
pdf_files = [
    "./path/to/your/document1.pdf",
    "./path/to/your/document2.pdf"
]
```

### Key API Patterns

**Create Vector Store:**
```python
vector_store = client.vector_stores.create(
    name="Research Papers",
    expires_after={
        "anchor": "last_active_at",
        "days": 7
    }
)
```

**Search with File Search Tool:**
```python
response = client.responses.create(
    input=query,
    model="gpt-4o-mini",
    instructions=instructions,
    tools=[{
        "type": "file_search",
        "vector_store_ids": [vector_store_id],
        "max_num_results": 5
    }]
)
```

**Continue Conversation:**
```python
response = client.responses.create(
    input=follow_up_query,
    previous_response_id=previous_response.id,
    tools=[{"type": "file_search", "vector_store_ids": [vs_id]}]
)
```

## Demo 2: Investment Suggestion Generator

**File:** `demo_2_investment_advisor.py`

### Description
An AI investment advisor that provides portfolio analysis, investment comparisons, and market insights using the Code Interpreter tool for data analysis and visualizations.

### Features
- Investment portfolio analysis
- Investment option comparisons
- Market outlook and trends
- Risk assessment and recommendations
- Data visualizations and calculations
- Interactive conversation mode
- Proper financial disclaimer

### Usage

```bash
# Run the demo
python demo_2_investment_advisor.py
```

### Example Scenarios

**1. General Investment Advice:**
```python
advisor.get_investment_suggestion(
    "I'm 30 years old with moderate risk tolerance. "
    "How should I allocate $10,000 for retirement?"
)
```

**2. Portfolio Analysis:**
```python
portfolio = {
    "age": 35,
    "risk_tolerance": "Moderate to Aggressive",
    "timeline": "25-30 years until retirement",
    "holdings": "60% stocks, 30% bonds, 10% cash",
    "goals": "Retirement savings"
}
advisor.analyze_portfolio(portfolio)
```

**3. Compare Investments:**
```python
advisor.compare_investments(
    investment_options=[
        "S&P 500 Index Fund",
        "Total Bond Market Fund",
        "Real Estate Investment Trust"
    ]
)
```

**4. Market Outlook:**
```python
advisor.market_outlook(sector="technology sector")
```

### Key API Patterns

**Using Code Interpreter:**
```python
response = client.responses.create(
    input=query,
    model="gpt-4o",
    instructions=instructions,
    tools=[{
        "type": "code_interpreter",
        "container": {"type": "auto"}
    }]
)
```

**Streaming Responses:**
```python
stream = client.responses.create(
    input=query,
    model="gpt-4o",
    instructions=instructions,
    tools=[{"type": "code_interpreter", "container": {"type": "auto"}}],
    stream=True
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
    elif event.type == "response.completed":
        conversation_id = event.response.id
```

## Prerequisites

### Environment Setup

1. **Install dependencies:**
   ```bash
   pip install openai
   ```

2. **Set up API key:**
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

   Or set it in your Python code:
   ```python
   client = OpenAI(api_key="your-api-key-here")
   ```

### Required Files (for PDF Search Demo)

Place your PDF documents in the repository:
```
notebooks/assets-resources/pdfs/
├── future_agents.pdf
└── attention_paper.pdf
```

## Architecture Comparison

### Old Way (Assistants API)
```python
# Create assistant
assistant = client.beta.assistants.create(
    instructions="You are helpful",
    tools=[{"type": "file_search"}]
)

# Create thread
thread = client.beta.threads.create()

# Add message
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Hello"
)

# Run assistant
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id
)
```

### New Way (Responses API)
```python
# Single call - much simpler!
response = client.responses.create(
    input="Hello",
    instructions="You are helpful",
    tools=[{
        "type": "file_search",
        "vector_store_ids": [vs_id]
    }]
)

# Continue conversation
response2 = client.responses.create(
    input="Follow up",
    previous_response_id=response.id,
    tools=[{"type": "file_search", "vector_store_ids": [vs_id]}]
)
```

## Benefits of Responses API

1. **Simpler Code:** Fewer API calls and objects to manage
2. **Better Performance:** Direct responses without polling
3. **Flexible State:** Use `previous_response_id` for context
4. **Unified Interface:** Same pattern for all tools
5. **Easier Debugging:** Clear request/response structure

## Cost Considerations

### File Search
- **Query cost:** $2.50 per 1,000 queries
- **Storage:** $0.10/GB/day (first GB free)
- **Tip:** Use `expires_after` to auto-cleanup

### Code Interpreter
- **Session cost:** $0.03 per session
- **Tip:** Efficient for data analysis and visualizations

### Token Usage
- `previous_response_id` loads full conversation history
- All prior tokens remain billable
- Use `truncation="auto"` for long conversations

## Best Practices

1. **Always include instructions** - They're stateless in Responses API
2. **Use streaming** for better user experience
3. **Set expiration policies** on vector stores to manage costs
4. **Handle errors gracefully** with try-catch blocks
5. **Clean up resources** when done (vector stores, files)
6. **Add appropriate disclaimers** (especially for financial/medical apps)

## Interactive Mode

Both demos include an interactive mode where you can:
- Ask custom questions
- Continue conversations naturally
- Type `quit` or `exit` to exit
- Type `reset` (Investment demo) to start fresh

## Troubleshooting

### PDF Upload Issues
- Ensure files exist at specified paths
- Check file size (max 512 MB)
- Supported formats: PDF, DOCX, TXT, MD, etc.

### API Errors
- Verify `OPENAI_API_KEY` is set correctly
- Check you have sufficient API credits
- Ensure you're using `openai>=2.6.1`

### Streaming Issues
- Flush output with `flush=True` for real-time display
- Handle all event types appropriately

## Related Notebooks

These demos are based on concepts from:
- `1.0-intro-openai-responses-api.ipynb` - Basic Responses API usage
- `2.0-managing-conversations.ipynb` - Conversation management
- `3.0-rag-docs.ipynb` - File Search and RAG patterns

## Resources

- [OpenAI Responses API Documentation](https://platform.openai.com/docs/api-reference/responses)
- [File Search Guide](https://platform.openai.com/docs/guides/tools-file-search)
- [Code Interpreter Guide](https://platform.openai.com/docs/guides/tools-code-interpreter)
- [Migration Guide](https://platform.openai.com/docs/assistants/migration)

## License

Educational use for O'Reilly Live Training course participants.

---

**Course:** Building AI Agents with OpenAI's Responses API
**Instructor:** [Your Name]
**Last Updated:** 2025-10-28
