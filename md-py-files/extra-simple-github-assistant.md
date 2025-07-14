# Simple GitHub Assistant

This notebook demonstrates how to create a GitHub assistant that can interact with GitHub repositories through the GitHub API using OpenAI's Assistants API.

## Setup and Authentication

First, let's set up the GitHub API connection:

```python
from github import Auth, Github
import os

auth = Auth.Token(os.getenv("GITHUB_ACCESS_TOKEN"))
g = Github(auth=auth)
g.get_user().login
```

Output:
```
'EnkrateiaLucca'
```

## Exploring Repository Contents

Let's explore the contents of a test repository:

```python
repo = g.get_repo("EnkrateiaLucca/test-repo")
repo.get_contents("")
```

Output:
```
[ContentFile(path=".gitignore"),
 ContentFile(path="Course-outline-gpt-assistants.md"),
 ContentFile(path="README.md"),
 ContentFile(path="test.txt"),
 ContentFile(path="testing_github_assistant.md")]
```

## Basic GitHub Operations

### Creating a File

```python
# Create a new file in the repository¶
repo.create_file("test2.txt", "test", "test", branch="main")
```

Output:
```
{'content': ContentFile(path="test2.txt"),
 'commit': Commit(sha="0879f20d692fa65142927415fa0b18b6f914bddf")}
```

### Updating a File

```python
# Update a file in the repository¶
contents = repo.get_contents("test2.txt", ref="main")
repo.update_file(contents.path, "more tests", "more tests", contents.sha, branch="main")
```

Output:
```
{'commit': Commit(sha="66f43ee8749d40247c1b237f942b8ab86780b74c"),
 'content': ContentFile(path="test2.txt")}
```

### Deleting a File

```python
# Delete a file in the repository
contents = repo.get_contents("test2.txt", ref="main")
repo.delete_file(contents.path, "deleting test", contents.sha, branch="main")
```

Output:
```
{'commit': Commit(sha="6489adcdbf9a43d7b62da69aa3a884d0738572de"),
 'content': NotSet}
```

## Creating Tool Functions

Let's create reusable tool functions for the assistant:

```python
def create_file_tool(repo_name, file_name, commit_msg, file_content, branch="main"):
    """
    Create a file in the repository
    """
    auth = Auth.Token(os.environ.get("GITHUB_ACCESS_TOKEN"))
    g = Github(auth=auth)
    repo = g.get_repo(f"EnkrateiaLucca/{repo_name}")
    repo.create_file(file_name, commit_msg, file_content, branch=branch)
    return f"File created successfully: {file_name}"

def update_file_tool(repo_name, file_name, commit_msg, file_content, branch="main"):
    """
    Update a file in the repository
    """
    auth = Auth.Token(os.environ.get("GITHUB_ACCESS_TOKEN"))
    g = Github(auth=auth)
    repo = g.get_repo(f"EnkrateiaLucca/{repo_name}")
    contents = repo.get_contents(file_name, ref=branch)
    repo.update_file(contents.path, commit_msg, file_content, contents.sha, branch=branch)
    return f"File updated successfully: {file_name}"
```

Test the tool functions:

```python
create_file_tool("test-repo", "test.txt", "test", "test", branch="main")
```

Output:
```
'File created successfully: test.txt'
```

```python
update_file_tool("test-repo", "test.txt", "testing pancakes", "again pancakes", branch="main")
```

Output:
```
'File updated successfully: test.txt'
```

## Creating the GitHub Assistant

Now let's create an assistant with GitHub capabilities:

```python
from openai import OpenAI

client = OpenAI()

my_assistant = client.beta.assistants.create(
    instructions="You are a GitHub assistant. You help users with github related tasks like commits, pull requests, and issues.",
    model="gpt-4o",
    name="GitHub Assistant",
    tools=[{"type": "file_search"}, 
            {"type": "code_interpreter"}, 
            {"type": "function",
             "function": {
                 "name": "create_file_tool",
                 "description": "Create a file in the repository",
                 "parameters": {
                     "type": "object",
                     "properties": {
                         "repo_name": {"type": "string", "description": "The name of the repository to create the file in"},
                         "file_name": {"type": "string", "description": "The name of the file to create"},
                         "commit_msg": {"type": "string", "description": "The commit message for the file"},
                         "file_content": {"type": "string", "description": "The content of the file to create"},
                         "branch": {"type": "string", "description": "The branch to create the file on", "default": "main"}
                     },
                     "required": ["repo_name", "file_name", "commit_msg", "file_content"]
                 }
             }
             },
             {
                 "type": "function",
                 "function": {
                     "name": "update_file_tool",
                     "description": "Update a file in the repository",
                     "parameters": {
                         "type": "object",
                         "properties": {
                             "repo_name": {"type": "string", "description": "The name of the repository to update"},
                             "file_name": {"type": "string", "description": "The name of the file to update"},
                             "commit_msg": {"type": "string", "description": "The commit message for the file"},
                             "file_content": {"type": "string", "description": "The content of the file to update"},
                             "branch": {"type": "string", "description": "The branch to update the file on", "default": "main"}
                         },
                         "required": ["repo_name", "file_name", "commit_msg", "file_content"]
                     }
                 }
             }
         ]
)

my_assistant.id
```

Output:
```
'asst_hQuthsXL7pc0fRJ1eHZ0q8Sj'
```

## Testing the Assistant

Create a thread and send a message:

```python
thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Create a new file called text.txt with the content 'Testing Github Assistant' on the main branch of test-repo?"
)

message.content[0].text.value
```

Output:
```
"Create a new file called text.txt with the content 'Testing Github Assistant' on the main branch of test-repo?"
```

## Tool Mapping

Create a mapping of tool names to their handler functions:

```python
tool_map = {
    "create_file_tool": lambda args: create_file_tool(**args),
    "update_file_tool": lambda args: update_file_tool(**args)
}
```

## Running the Assistant with Tools

Create a helper function to run the assistant with tool handling:

```python
import json

def run_assistant_with_tools(client, thread_id, assistant_id, tool_map=None):
    """
    Run an assistant with tool handling capabilities.
    
    Args:
        client: OpenAI client instance
        thread_id: ID of the thread to run
        assistant_id: ID of the assistant to use
        tool_map: Dictionary mapping tool names to their handler functions
    
    Returns:
        The messages from the completed run, or None if unsuccessful
    """
    
    if tool_map is None:
        tool_map = {}
        
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
        return messages
        
    elif run.status == 'requires_action':
        tool_outputs = []

        for tool in run.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name in tool_map:
                tool_outputs.append({
                    "tool_call_id": tool.id,
                    "output": tool_map[tool.function.name](json.loads(tool.function.arguments))
                })

        if tool_outputs:
            try:
                run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=thread_id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
                
                if run.status == 'completed':
                    messages = client.beta.threads.messages.list(
                        thread_id=thread_id
                    )
                    return messages
                else:
                    return None
                    
            except Exception as e:
                print(f"Failed to submit tool outputs: {e}")
                return None
                
        return None
        
    return None

# Example usage:    
messages = run_assistant_with_tools(client, thread.id, my_assistant.id, tool_map)
if messages:
    print(messages)
```

Output:
```
SyncCursorPage[Message](data=[Message(id='msg_UDr8BvD83kDrH4yyWinRjYX8', assistant_id='asst_hQuthsXL7pc0fRJ1eHZ0q8Sj', attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], value="The file `text.txt` has been successfully created in the `test-repo` repository on the main branch with the content 'Testing Github Assistant'."), type='text')], created_at=1736794374, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='assistant', run_id='run_IVr13CG2xlTbDzQIDSewMFLE', status=None, thread_id='thread_ZKeiukgZV6xGOQQPYuNPkLVo'), Message(id='msg_gMJfPjuKtsqsqJrqGXZRGR0V', assistant_id=None, attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], value="Create a new file called text.txt with the content 'Testing Github Assistant' on the main branch of test-repo?"), type='text')], created_at=1736794362, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='user', run_id=None, status=None, thread_id='thread_ZKeiukgZV6xGOQQPYuNPkLVo')], object='list', first_id='msg_UDr8BvD83kDrH4yyWinRjYX8', last_id='msg_gMJfPjuKtsqsqJrqGXZRGR0V', has_more=False)
```

## Getting the Final Response

```python
messages.data[0].content[0].text.value
```

Output:
```
"The file `text.txt` has been successfully created in the `test-repo` repository on the main branch with the content 'Testing Github Assistant'."
```

## Summary

This notebook demonstrates how to create a GitHub assistant that can:

1. **Authenticate with GitHub**: Use GitHub API tokens to access repositories
2. **Perform Repository Operations**: Create, update, and delete files
3. **Create Tool Functions**: Wrap GitHub operations in reusable functions
4. **Integrate with OpenAI Assistant**: Use function calling to execute GitHub operations
5. **Handle Tool Execution**: Properly handle the `requires_action` status and tool outputs

The assistant can understand natural language requests and execute the appropriate GitHub operations, making it easy to manage repositories through conversational interfaces.

Key features demonstrated:
- File creation and updates in GitHub repositories
- Function calling integration with OpenAI Assistants API
- Error handling and tool output management
- Reusable tool mapping for different GitHub operations

This pattern can be extended to support more GitHub operations like creating issues, pull requests, managing branches, and more.