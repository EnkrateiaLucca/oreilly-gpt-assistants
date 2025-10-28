# Quick Start Guide - Demo Applications

## 🚀 Get Started in 3 Steps

### Step 1: Set Your API Key

```bash
export OPENAI_API_KEY='your-api-key-here'
```

### Step 2: Run the Tests

```bash
python test_demos.py
```

You should see:
```
🎉 All tests passed! Demos are ready to use.
```

### Step 3: Run the Demos

**Option A: PDF Document Search**
```bash
python demo_1_pdf_search.py
```

**Option B: Investment Advisor**
```bash
python demo_2_investment_advisor.py
```

---

## 📋 What Each Demo Does

### Demo 1: PDF Document Search
- Uploads research papers to a vector store
- Answers questions about the papers using natural language
- Maintains conversation context for follow-up questions
- **Try asking:** "What is the attention mechanism?"

### Demo 2: Investment Advisor
- Analyzes investment portfolios
- Compares investment options
- Provides market insights
- Creates visualizations using code interpreter
- **Try asking:** "How should I diversify my retirement portfolio?"

---

## 💡 Key Concepts Demonstrated

Both demos showcase the **OpenAI Responses API**, which is:
- ✅ **Simpler** than the old Assistants API
- ✅ **Faster** with better performance
- ✅ **More flexible** with stateless design
- ✅ **Easier** to maintain conversations

### Core Pattern

```python
# 1. Create a response
response = client.responses.create(
    input="Your question",
    model="gpt-4o",
    instructions="System instructions",
    tools=[{"type": "file_search"}]  # or "code_interpreter"
)

# 2. Continue the conversation
response2 = client.responses.create(
    input="Follow-up question",
    previous_response_id=response.id,  # This maintains context!
    tools=[{"type": "file_search"}]
)
```

That's it! No threads, no polling, no complex state management.

---

## 🎯 Interactive Mode

Both demos have an interactive mode:

```bash
# After the examples run, you'll see:
Your question: _

# Try these:
- "Summarize the key findings"
- "Compare different approaches"
- "What are the risks?"

# To exit:
quit
```

---

## 📊 What You'll See

### PDF Search Demo Output:
```
===========================================================
Query: What is the main topic of these papers?
===========================================================
Response: The papers discuss advances in AI agents and
the attention mechanism in neural networks...
[Continues with detailed response]
===========================================================
```

### Investment Advisor Output:
```
===========================================================
Query: How should I allocate my portfolio?
===========================================================
Investment Advisor: Based on your profile...

[Running analysis...]

[May include code execution and visualizations]
===========================================================
```

---

## 🛠️ Customization

### Add Your Own PDFs (Demo 1)

Edit `demo_1_pdf_search.py`:

```python
pdf_files = [
    "./path/to/your/document1.pdf",
    "./path/to/your/document2.pdf"
]
```

### Change Analysis Depth (Demo 2)

Edit `demo_2_investment_advisor.py`:

```python
# Use different models
model="gpt-4o"        # More powerful, better analysis
model="gpt-4o-mini"   # Faster, more cost-effective

# Enable/disable code interpreter
use_code_interpreter=True   # For calculations and charts
use_code_interpreter=False  # For text-only responses
```

---

## 💰 Cost Estimates

### Demo 1 (PDF Search)
- Vector store: ~$0.01/day (first GB free)
- Queries: ~$0.0025 per query
- **Total for testing:** < $0.10

### Demo 2 (Investment Advisor)
- Code interpreter: $0.03 per session
- Token usage: ~$0.01-0.05 per query
- **Total for testing:** < $0.50

**Total cost to run both demos:** Less than $1 🎉

---

## 🔍 Troubleshooting

### "Module not found" error
```bash
pip install openai
```

### "API key not set" error
```bash
# Set it in your terminal
export OPENAI_API_KEY='sk-...'

# Or in Python
import os
os.environ["OPENAI_API_KEY"] = "sk-..."
```

### "File not found" error (Demo 1)
```bash
# Check if PDFs exist
ls -l notebooks/assets-resources/pdfs/

# Update paths in demo_1_pdf_search.py if needed
```

### Rate limit errors
- Wait a few seconds between requests
- Or upgrade your OpenAI plan

---

## 📚 Learn More

- Full documentation: `DEMOS_README.md`
- Course notebooks: `notebooks/`
  - `1.0-intro-openai-responses-api.ipynb`
  - `2.0-managing-conversations.ipynb`
  - `3.0-rag-docs.ipynb`

---

## 🎓 Course Wrap-Up

### What We've Learned:

1. **Responses API Basics**
   - Creating responses
   - Managing conversations
   - Streaming output

2. **Built-in Tools**
   - File Search for document Q&A
   - Code Interpreter for analysis

3. **Real Applications**
   - Research assistant (Demo 1)
   - Financial advisor (Demo 2)

### Next Steps:

1. **Modify** these demos for your use case
2. **Combine** tools for more powerful apps
3. **Build** your own AI applications!

---

## 🤝 Support

Questions? Issues?
- Check `DEMOS_README.md` for detailed docs
- Review the course notebooks
- Consult OpenAI's [API documentation](https://platform.openai.com/docs)

---

**Happy Building! 🚀**

Built with ❤️ for O'Reilly Live Training
