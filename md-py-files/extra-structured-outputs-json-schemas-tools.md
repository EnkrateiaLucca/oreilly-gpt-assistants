# Structured Outputs JSON Schemas Tools

This notebook demonstrates how to create structured outputs and JSON schemas for tools using Pydantic models with OpenAI's Assistants API.

## Creating Structured Tool Schemas

Using Pydantic models, we can create structured schemas for tools that ensure consistent input/output formats:

```python
from pydantic import BaseModel, Field

class ExampleToolStructured(BaseModel):
    attribute1: str = Field(description="Some attribute")
    attribute2: str = Field(description="Another attribute")
    
file_search_tool = ExampleToolStructured(attribute1="test.txt", attribute2="test")

file_search_tool.model_json_schema()
```

Output:
```python
{'properties': {'attribute1': {'description': 'Some attribute',
   'title': 'Attribute1',
   'type': 'string'},
  'attribute2': {'description': 'Another attribute',
   'title': 'Attribute2',
   'type': 'string'}},
 'required': ['attribute1', 'attribute2'],
 'title': 'ExampleToolStructured',
 'type': 'object'}
```

## Benefits of Structured Outputs

1. **Type Safety**: Ensures inputs and outputs conform to expected types
2. **Clear Documentation**: Field descriptions provide clear parameter documentation
3. **Validation**: Automatic validation of data structures
4. **IDE Support**: Better autocomplete and error detection
5. **Consistency**: Standardized format across all tools

## Example Tool Implementations

Here are some examples of how to implement structured tools:

### File Search Tool

```python
class FileSearchTool(BaseModel):
    query: str = Field(description="Search query for finding files")
    file_types: List[str] = Field(description="List of file types to search for", default=[])
    max_results: int = Field(description="Maximum number of results to return", default=10)
```

### Email Tool

```python
class EmailTool(BaseModel):
    to: str = Field(description="Recipient email address")
    subject: str = Field(description="Email subject line")
    body: str = Field(description="Email body content")
    attachments: List[str] = Field(description="List of attachment file paths", default=[])
```

### Calendar Event Tool

```python
class CalendarEventTool(BaseModel):
    title: str = Field(description="Event title")
    start_time: str = Field(description="Start time in ISO format")
    end_time: str = Field(description="End time in ISO format")
    description: str = Field(description="Event description", default="")
    location: str = Field(description="Event location", default="")
    attendees: List[str] = Field(description="List of attendee email addresses", default=[])
```

## Integration with OpenAI Assistants API

To use these structured schemas with the Assistants API, you would convert them to the required JSON format:

```python
def create_assistant_with_structured_tools():
    assistant = client.beta.assistants.create(
        name="Structured Tools Assistant",
        instructions="You are an assistant that uses structured tools for consistent data handling.",
        model="gpt-4o",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "file_search_tool",
                    "description": "Search for files based on criteria",
                    "parameters": FileSearchTool.model_json_schema()
                }
            },
            {
                "type": "function", 
                "function": {
                    "name": "email_tool",
                    "description": "Send emails with structured data",
                    "parameters": EmailTool.model_json_schema()
                }
            }
        ]
    )
    return assistant
```

## Best Practices

1. **Use Descriptive Field Names**: Make field names self-explanatory
2. **Provide Clear Descriptions**: Include helpful descriptions for each field
3. **Set Appropriate Defaults**: Use sensible default values where applicable
4. **Use Type Hints**: Leverage Python's type system for better validation
5. **Validate Data**: Use Pydantic's validation features to ensure data integrity

## Summary

Structured outputs with JSON schemas provide a robust framework for building consistent, well-documented tools in OpenAI's Assistants API. By using Pydantic models, you can:

- Ensure type safety and data validation
- Generate clear, consistent API documentation
- Improve development experience with better IDE support
- Maintain consistency across different tools and functions

This approach is particularly valuable in production environments where reliability and maintainability are crucial.