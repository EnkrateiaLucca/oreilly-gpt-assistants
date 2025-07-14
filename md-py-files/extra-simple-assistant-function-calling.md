# Simple Assistant Function Calling

This notebook demonstrates how to create a simple assistant with function calling capabilities, specifically for web searching using the SerpAPI.

## Setting Up Web Search Function

First, let's create a web search function using SerpAPI:

```python
import os
from serpapi import GoogleSearch

serpapi_params = {
    "api_key": os.getenv("SERPAPI_KEY"),
}

def web_search(query):
    """
    Perform a web search using the SerpAPI Google Search API.
    """
    search = GoogleSearch({
        **serpapi_params,
        "q": query,
        "num": 5
    })

    return search.get_dict()["organic_results"]

output_search = web_search("What are the top 3 hikes Ireland that take less than 6 hours?")
```

Test the search function:

```python
output_search[0]["snippet"]
```

Output:
```
'1. Torc Waterfall Trail · #1 - Torc Waterfall Trail · 4.7 ; 2. Lower Diamond Hill (Blue Route). #2 - Lower Diamond Hill (Blue Route) · 4.7 ; 3. Ballinastoe Wood.'
```

## Formatting Search Results

Create a function to format search results:

```python
def format_search_results(search_results):
    """
    Processes the search results and returns a formatted string containing
    the title, url, and snippet for each resource, separated by skipping lines.
    """
    formatted_results = []
    for result in search_results:
        title = result.get('title', 'No title')
        url = result.get('link', 'No URL')
        snippet = result.get('snippet', 'No snippet')
        formatted_results.append(f"Title: {title}\nURL: {url}\nSnippet: {snippet}\n")

    return "\n".join(formatted_results)

formatted_search_results = format_search_results(output_search)
formatted_search_results
```

Output:
```
Title: 10 Best short trails in Ireland
URL: https://www.alltrails.com/ireland/short
Snippet: 1. Torc Waterfall Trail · #1 - Torc Waterfall Trail · 4.7 ; 2. Lower Diamond Hill (Blue Route). #2 - Lower Diamond Hill (Blue Route) · 4.7 ; 3. Ballinastoe Wood.

Title: Ireland's Top 10 Scenic Hikes for Beginners
URL: https://blog.irishtourism.com/2024/06/06/irelands-top-10-scenic-hikes-for-beginners/
Snippet: Torc Waterfall Walk, Killarney National Park, County Kerry · Lower Diamond Hill, near Letterfrack village, Connemara National Park, County Galway.

Title: Ireland's Ancient East – 10 day-hikes to explore in the region
URL: https://blog.hiiker.app/2021/11/25/irelands-ancient-east-10-day-hikes-to-explore-in-the-region/
Snippet: Ireland's Ancient East – 10 day-hikes to explore in the region · 1. Tonelagee (Lough Ouler), Co. Wicklow · 2. Mullaghcleevaun & Cleevaun Lough, Co ...

Title: Ultimate Guide to Multi-Day Walks in Ireland
URL: https://www.kimkim.com/c/ultimate-guide-to-multi-day-walks-in-ireland
Snippet: The famous eight-day Ring of Kerry circuit takes hikers around the stunning cliffs, hidden beaches, and quaint towns of Ireland's Wild Atlantic Way.

Title: 3 Days of Hiking - Recommendations Please! - Ireland Forum
URL: https://www.tripadvisor.com/ShowTopic-g186591-i88-k10386319-3_Days_of_Hiking_Recommendations_Please-Ireland.html
Snippet: I'd stick with the Wicklow Way if I were you. Never more than a half hour without company. http://www.wicklowway.com/.
```

## Creating the Search Tool Function

```python
def search_tool(query):
    """
    Search the web for information on a given topic and return a formatted string
    containing the title, url, and snippet for each resource.
    """
    return format_search_results(web_search(query))
```

## Creating the Assistant

Now let's create an assistant with function calling capabilities:

```python
from openai import OpenAI

client = OpenAI()

my_assistant = client.beta.assistants.create(
    instructions="You are a web research assistant. You ALWAYS use the search tool to search the web and create an organized markdown style reports for any topic.",
    model="gpt-4o",
    name="Web Research Assistant",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "search_tool",
                "description": "Search the web for information on a given topic",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query to search the web for"
                        }
                    },
                    "required": ["query"]
                }
            }
        },
        {"type": "code_interpreter"},
        {"type": "file_search"}
    ]
)

my_assistant.id
```

Output:
```
'asst_C2YRbEAw5hybBhAc2dsd2drU'
```

## Testing the Assistant

Create a thread and send a message:

```python
thread = client.beta.threads.create()
message= client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Search online for the top 5 activities to do in Ireland."
)

message.content[0].text.value
```

Output:
```
'Search online for the top 5 activities to do in Ireland.'
```

## Running the Assistant with Function Calling

```python
import json

run = client.beta.threads.runs.create_and_poll(
thread_id=thread.id,
assistant_id=my_assistant.id,
)

if run.status == 'completed':
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    print(messages)
elif run.status == 'requires_action':
    # Define the list to store tool outputs
    tool_outputs = []

    # Loop through each tool in the required action section
    for tool in run.required_action.submit_tool_outputs.tool_calls:
        if tool.function.name == "search_tool":
            # For web search, we'll pass through the function arguments as output
            tool_outputs.append({
                "tool_call_id": tool.id,
                "output": search_tool(json.loads(tool.function.arguments)['query'])
            })

    # Submit all tool outputs at once after collecting them in a list
    if tool_outputs:
        try:
            run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
            print("Tool outputs submitted successfully.")
            
            if run.status == 'completed':
                messages = client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                print(messages)
            else:
                print(run.status)
                
        except Exception as e:
            print("Failed to submit tool outputs:", e)
    else:
        print("No tool outputs to submit.")
else:
    print(run.status)
```

Output:
```
Tool outputs submitted successfully.
SyncCursorPage[Message](data=[Message(id='msg_VVl8R6I3OiPp2BgwJF8wLFIh', assistant_id='asst_C2YRbEAw5hybBhAc2dsd2drU', attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], value="Here are some top activities to do in Ireland based on popular travel resources:\n\n1. **Visit Kilmainham Gaol Museum**: Discover Irish history at this historic jail in Dublin, which has played a significant role in the country's path to independence .\n\n2. **Explore the Guinness Storehouse**: Learn about Ireland's most famous beer at this immersive museum located at St. James's Gate Brewery in Dublin .\n\n3. **Travel the Ring of Kerry**: Experience breathtaking landscapes and picturesque towns along this famous scenic drive in County Kerry .\n\n4. **Discover Yeats Country**: Visit the areas associated with the famous poet W.B. Yeats, particularly around Sligo, known for its beautiful landscapes .\n\n5. **Experience the Wild Atlantic Way**: Enjoy the stunning coastline of Ireland with activities such as swimming, hiking, and visiting quaint towns along this spectacular route .\n\nThese activities offer a mix of cultural, historical, and natural experiences that showcase the diversity of Ireland."), type='text')], created_at=1736699086, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='assistant', run_id='run_uQVcKgslr5wByINDsHmh2OBX', status=None, thread_id='thread_SaX44Ah98o2PGiWZDCmDhy9M'), Message(id='msg_ezzAK1Bkq6IHiGhzao504k6W', assistant_id=None, attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], value='Search online for the top 5 activities to do in Ireland.'), type='text')], created_at=1736699078, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='user', run_id=None, status=None, thread_id='thread_SaX44Ah98o2PGiWZDCmDhy9M')], object='list', first_id='msg_VVl8R6I3OiPp2BgwJF8wLFIh', last_id='msg_ezzAK1Bkq6IHiGhzao504k6W', has_more=False)
```

## Getting the Final Response

```python
messages.data[0].content[0].text.value
```

Output:
```
"Here are some top activities to do in Ireland based on popular travel resources:

1. **Visit Kilmainham Gaol Museum**: Discover Irish history at this historic jail in Dublin, which has played a significant role in the country's path to independence .

2. **Explore the Guinness Storehouse**: Learn about Ireland's most famous beer at this immersive museum located at St. James's Gate Brewery in Dublin .

3. **Travel the Ring of Kerry**: Experience breathtaking landscapes and picturesque towns along this famous scenic drive in County Kerry .

4. **Discover Yeats Country**: Visit the areas associated with the famous poet W.B. Yeats, particularly around Sligo, known for its beautiful landscapes .

5. **Experience the Wild Atlantic Way**: Enjoy the stunning coastline of Ireland with activities such as swimming, hiking, and visiting quaint towns along this spectacular route .

These activities offer a mix of cultural, historical, and natural experiences that showcase the diversity of Ireland."
```

## Summary

This notebook demonstrates how to create a simple assistant with function calling capabilities. The key components include:

1. **Web Search Function**: Using SerpAPI to search the web
2. **Result Formatting**: Processing search results into a readable format
3. **Assistant Creation**: Setting up an assistant with function calling tools
4. **Function Execution**: Handling `requires_action` status to execute functions
5. **Response Processing**: Getting the final formatted response from the assistant

The assistant can take user queries, search the web for relevant information, and provide organized, markdown-formatted reports based on the search results.