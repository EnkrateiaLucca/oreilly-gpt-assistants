# assistants.py - OpenAI Assistants API Integration

This file provides the core functionality for processing user queries through OpenAI's Assistants API and handling various tools including Gmail and Google Calendar integration.

## Overview

The module handles:
- Creating and managing OpenAI Assistant threads
- Processing user queries with function calling
- Managing file uploads and downloads
- Integrating with Gmail and Google Calendar tools
- Returning structured responses with text and files

## Dependencies

```python
import os
import json
import openai
from time import sleep
from dotenv import load_dotenv
import io  # Import for in-memory file handling
from tools import read_emails, send_email, list_events, create_event, update_event, delete_event
```

## Configuration

```python
# Load your OpenAI API key from the .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
```

## Function Execution Handler

The `execute_function` function maps function names to their corresponding implementations:

```python
def execute_function(function_name, arguments, from_user):
    """
    Execute a function based on the function name and provided arguments.
    """
    if function_name == 'read_emails':
        query = arguments.get("query", "in:inbox")
        max_results = arguments.get("max_results", 10)
        return read_emails(query=query, max_results=max_results)
    elif function_name == 'send_email':
        to = arguments.get("to")
        subject = arguments.get("subject")
        body = arguments.get("body")
        attachments = arguments.get("attachments")
        return send_email(to=to, subject=subject, body=body, attachments=attachments)
    # Google Calendar functions
    elif function_name == 'list_events':
        max_results = arguments.get("max_results", 10)
        time_min = arguments.get("time_min")
        time_max = arguments.get("time_max")
        calendar_id = arguments.get("calendar_id", "primary")
        return list_events(max_results=max_results, time_min=time_min, 
                          time_max=time_max, calendar_id=calendar_id)
    elif function_name == 'create_event':
        summary = arguments.get("summary")
        start_time = arguments.get("start_time")
        end_time = arguments.get("end_time")
        description = arguments.get("description", "")
        location = arguments.get("location", "")
        attendees = arguments.get("attendees")
        calendar_id = arguments.get("calendar_id", "primary")
        return create_event(summary=summary, start_time=start_time, end_time=end_time,
                           description=description, location=location, 
                           attendees=attendees, calendar_id=calendar_id)
    elif function_name == 'update_event':
        event_id = arguments.get("event_id")
        summary = arguments.get("summary")
        start_time = arguments.get("start_time")
        end_time = arguments.get("end_time")
        description = arguments.get("description")
        location = arguments.get("location")
        attendees = arguments.get("attendees")
        calendar_id = arguments.get("calendar_id", "primary")
        return update_event(event_id=event_id, summary=summary, start_time=start_time,
                           end_time=end_time, description=description, location=location,
                           attendees=attendees, calendar_id=calendar_id)
    elif function_name == 'delete_event':
        event_id = arguments.get("event_id")
        calendar_id = arguments.get("calendar_id", "primary")
        return delete_event(event_id=event_id, calendar_id=calendar_id)
    else:
        return "Function not recognized"
```

## Main Thread Processing Function

The core function that processes user queries through the OpenAI Assistants API:

```python
def process_thread_with_assistant(user_query, assistant_id, model="gpt-4o", from_user=None):
    """
    Process a thread with an assistant and handle the response which includes text and images.

    :param user_query: The user's query.
    :param assistant_id: The ID of the assistant to be used.
    :param model: The model version of the assistant.
    :param from_user: The user ID from whom the query originated.
    :return: A dictionary containing text responses and in-memory file objects.
    """
    response_texts = []  # List to store text responses
    response_files = []  # List to store file IDs
    in_memory_files = []  # List to store in-memory file objects

    try:
        print("Creating a thread for the user query...")
        thread = openai.Client().beta.threads.create()
        print(f"Thread created with ID: {thread.id}")

        print("Adding the user query as a message to the thread...")
        openai.Client().beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_query
        )
        print("User query added to the thread.")

        print("Creating a run to process the thread with the assistant...")
        run = openai.Client().beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id,
            model=model
        )
        print(f"Run created with ID: {run.id}")

        while True:
            print("Checking the status of the run...")
            run_status = openai.Client().beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            print(f"Current status of the run: {run_status.status}")

            if run_status.status == "requires_action":
                print("Run requires action. Executing specified function...")
                tool_call = run_status.required_action.submit_tool_outputs.tool_calls[0]
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                function_output = execute_function(function_name, arguments, from_user)
                function_output_str = json.dumps(function_output)

                print("Submitting tool outputs...")
                openai.Client().beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=[{
                        "tool_call_id": tool_call.id,
                        "output": function_output_str
                    }]
                )
                print("Tool outputs submitted.")

            elif run_status.status in ["completed", "failed", "cancelled"]:
                print("Fetching messages added by the assistant...")
                messages = openai.Client().beta.threads.messages.list(thread_id=thread.id)
                for message in messages.data:
                    if message.role == "assistant":
                        for content in message.content:
                            if content.type == "text":
                                response_texts.append(content.text.value)
                            elif content.type == "image_file":
                                file_id = content.image_file.file_id
                                response_files.append(file_id)

                print("Messages fetched. Retrieving content for each file ID...")
                for file_id in response_files:
                    try:
                        print(f"Retrieving content for file ID: {file_id}")
                        # Retrieve file content from OpenAI API
                        file_response = openai.Client().files.content(file_id)
                        if hasattr(file_response, 'content'):
                            # If the response has a 'content' attribute, use it as binary content
                            file_content = file_response.content
                        else:
                            # Otherwise, use the response directly
                            file_content = file_response

                        in_memory_file = io.BytesIO(file_content)
                        in_memory_files.append(in_memory_file)
                        print(f"In-memory file object created for file ID: {file_id}")
                    except Exception as e:
                        print(f"Failed to retrieve content for file ID: {file_id}. Error: {e}")

                break
            sleep(1)

        return {"text": response_texts, "in_memory_files": in_memory_files}

    except Exception as e:
        print(f"An error occurred: {e}")
        return {"text": [], "in_memory_files": []}
```

## Key Features

### 1. **Thread Management**
- Creates new threads for each user query
- Manages thread lifecycle from creation to completion
- Handles thread status monitoring

### 2. **Function Calling**
- Supports multiple function types (Gmail, Calendar)
- Handles function argument parsing and execution
- Manages tool outputs submission

### 3. **File Processing**
- Retrieves generated files from OpenAI API
- Converts files to in-memory objects for easy handling
- Supports both text and image file types

### 4. **Error Handling**
- Comprehensive error handling throughout the process
- Graceful failure handling with meaningful error messages
- Fallback responses for various failure scenarios

## Supported Functions

### Gmail Functions
- `read_emails`: Read emails from Gmail inbox
- `send_email`: Send emails with optional attachments

### Google Calendar Functions
- `list_events`: List upcoming calendar events
- `create_event`: Create new calendar events
- `update_event`: Update existing calendar events
- `delete_event`: Delete calendar events

## Return Format

The function returns a dictionary containing:
- `text`: List of text responses from the assistant
- `in_memory_files`: List of in-memory file objects for generated files

## Usage Example

```python
# Example usage
user_query = "Hi"
assistant_id = "asst_qPkFH6kDCiYuCXZgW259VyDb"
response = process_thread_with_assistant(user_query, assistant_id)
print("Final response:", response)
```

This module provides a robust foundation for integrating OpenAI's Assistants API with various external tools and services.