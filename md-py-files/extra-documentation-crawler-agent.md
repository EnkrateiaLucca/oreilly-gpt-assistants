# Documentation Crawler Agent

This notebook demonstrates how to create a documentation crawler agent that can scrape web content and create a searchable knowledge base using OpenAI's Assistants API.

## Setup

```python
import os
import getpass

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"var: ")

_set_env("OPENAI_API_KEY")
```

## Web Scraping

Let's scrape content from a webpage about LLM agents:

```python
import requests
from bs4 import BeautifulSoup

# URL of the Webpage to scrape
url = "https://www.promptingguide.ai/research/llm-agents"

# Headers to mimic a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Send a GET request to the URL
response = requests.get(url, headers=headers, timeout=10)

print(response)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract the desired information from the HTML
    # For example, to get the repository name
    webpage_content = soup.get_text()
    
    # Print the repository name
    print("Webpage content:\n\n", webpage_content)
else:
    print("Failed to retrieve the webpage")
```

Save the scraped content to a file:

```python
with open("webpage_content.md", "w") as f:
    f.write(webpage_content)
```

## Creating the Assistant

Initialize the OpenAI client and create the assistant:

```python
from openai import OpenAI

client = OpenAI()
```

```python
file = client.files.create(
    file=open("webpage_content.md", "rb"),
    purpose="assistants"
)

assistant = client.beta.assistants.create(
    name="AI Agents Expert",
    description="You are an expert at AI Agents and can answer questions about them.",
    tools=[{"type": "file_search"}],
    model="gpt-4o",
)
```

## Setting Up Vector Store

Create a vector store and upload the scraped content:

```python
vector_store = client.beta.vector_stores.create(name="AI Agents Research")

file_paths = ["./webpage_content.md"]

file_streams = [open(file_path, "rb") for file_path in file_paths]

file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
vector_store_id=vector_store.id, files=file_streams
)

print(file_batch.status)
print(file_batch.id)
```

Output:
```
completed
vsfb_bda2eb04db1c4b18a482adbd92fc976d
```

Check the file upload status:

```python
print(file_batch.file_counts)
```

Output:
```
FileCounts(cancelled=0, completed=1, failed=0, in_progress=0, total=1)
```

## Updating the Assistant

Update the assistant with the vector store:

```python
# Let's update the assistant with the new vector store
assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
```

## Alternative: Attaching Files Directly to Thread

You can also attach files directly to a thread, which creates its own vector store:

```python
# Optionally we could attach the files directly in the thread
# This would create its own vector store if no other vector store is already attached
# to the assistant

# Upload the user provided file to OpenAI
# message_file = client.files.create(
# file=open("edgar/aapl-10k.pdf", "rb"), purpose="assistants"
# )

# # Create a thread and attach the file to the message
# thread = client.beta.threads.create(
# messages=[
#   {
#     "role": "user",
#     "content": "How many shares of AAPL were outstanding at the end of of October 2023?",
#     # Attach the new file to the message.
#     "attachments": [
#       { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
#     ],
#   }
# ]
# )

# # The thread now has a vector store with that file in its tool resources.
# print(thread.tool_resources.file_search)
```

## Testing the Agent

Create a thread and ask a question:

```python
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "What are the core components of an LLM Agent framework?"
        }
    ]
)

print(thread.id)
```

Output:
```
thread_RanfLa8BqW08RiJe9qpBeHIN
```

## Running the Assistant

Create a run and check the output:

```python
# Let's create a run and check the output
# First without streaming

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id, assistant_id=assistant.id
)

print(run)

if run.status == 'completed': 
    messages = client.beta.threads.messages.list(
    thread_id=thread.id
    )
    print(messages)
else:
    print(run.status)
```

Get the assistant's response:

```python
messages.data[0].content[0].text.value
```

Output:
```
"The core components of an LLM Agent framework typically include:

1. **User Request**: The initial input or question posed by the user.
   
2. **Agent/Brain**: The central component that acts as the coordinator. It is the large language model (LLM) responsible for processing the user request and orchestrating the overall operations.
   
3. **Planning**: A module to assist the agent in planning future actions. It helps in decomposing tasks and creating a detailed plan of subtasks necessary to address the user request. Planning can be enhanced with feedback to iteratively refine the plan based on past performance【4:0†source】.

4. **Memory**: This component manages the agent's past behaviors and interactions. It typically includes two types of memory:
   - **Short-term Memory**: Contextual information about the agent's current situation, often hindered by context window constraints.
   - **Long-term Memory**: Retention and recall of past behaviors and experiences over an extended period, usually leveraging external vector storage for efficient retrieval【4:0†source】."
```

## Handling File Citations

Here's an example of how to handle file citations in responses:

```python
# Example where we include file citations

# run = client.beta.threads.runs.create_and_poll(
#   thread_id=thread.id, assistant_id=assistant.id
# )

# messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

# message_content = messages[0].content[0].text
# annotations = message_content.annotations
# citations = []
# for index, annotation in enumerate(annotations):
#   message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
#   if file_citation := getattr(annotation, "file_citation", None):
#       cited_file = client.files.retrieve(file_citation.file_id)
#       citations.append(f"[{index}] {cited_file.filename}")

# print(message_content.value)
# print("\n".join(citations))
```

## Summary

This documentation crawler agent demonstrates how to:

1. **Web Scraping**: Extract content from web pages using requests and BeautifulSoup
2. **Content Storage**: Save scraped content to files for processing
3. **Vector Store Creation**: Create and manage vector stores for file search
4. **Assistant Configuration**: Set up assistants with file search capabilities
5. **Knowledge Querying**: Ask questions about the scraped content with proper citations

The agent can be extended to crawl multiple pages, handle different content types, and provide more sophisticated search and analysis capabilities.