#!/usr/bin/env python
# coding: utf-8

# # Can you SEE MY SCREEN?

# <span style="color: red;"> 
# How do we connect LLMs with Tools?
# </span>
# 

# In[2]:


from openai import OpenAI
import os

client = OpenAI()

# if you don't have an API key as an environment variable you can set it here

# os.environ["OPENAI_API_KEY"] = ""


# In[3]:


def llm_response(prompt: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

llm_response("How do we connect LLMs with Tools?")


# We could ask the model to:
# 
# 1. Generate Python code and then give the model the ability to run that code somewhere
# 2. Create the Python function that executes the task, then somehow give the model the ability to run that function autonomously

# Option number 2 is what we call FUNCTION CALLING!

# # Function Calling from Scratch
# 
# 1. Write a Python function
# 2. Make that function "available" to the LLM model of choice (in this case will be gpt-4o/gpt-4o-mini)
# 3. Test if the model can execute that function properly
#    1. Prepare the payload for the function (the arguments for it...)
#    2. Write the function call
#    3. We run the function call ourselves
#    4. We inspect the results

# In[4]:


def create_folder(folder_path: str):
    os.makedirs(folder_path, exist_ok=True)
    return f"Folder created at {folder_path}"

create_folder("./pancakes-are-the-best")


# In[7]:


get_ipython().system('ls -d ./* | grep pancakes')


# In[8]:


def write_file(file_path: str, content: str):
    with open(file_path, "w") as file:
        file.write(content)
    return f"File created at {file_path}"

write_file("./pancakes-are-the-best/pancakes-are-the-best.txt", "Pancakes are the best!")


# In[9]:


get_ipython().system('cat pancakes-are-the-best/pancakes-are-the-best.txt')


# # LLM + Python Functions

# The most silly way possible first!

# In[11]:


prompt_with_function_information = """
You are a personal assistant with desktop capabilities. 
Users will ask you to perform tasks and you will execute those tasks by calling one or more of the following functions:

- create_folder(folder_path: str)
- write_file(file_path: str, content: str)

For example if the user asks: 

'Create a folder called lucas-teaches-function-callling'

Your output should be code like this:
'create_folder("./lucas-teaches-function-callling")'

'Create a folder called pancakes-are-the-best and write a file called pancakes-are-the-best.txt with the content "Pancakes are the best!"'

Your output should be code like this:

['create_folder("./pancakes-are-the-best")', 'write_file("./pancakes-are-the-best/pancakes-are-the-best.txt", "Pancakes are the best!")']

Your OUTPUT should ALWAYS BE python code only.

Here is the user prompt:
"""


user_prompt = "Create a file named pancakes-are-better-than-waffles.md with a one paragraph summary for why pancakes are better, \
make sure to address RS a student from my course who dared to say avocado waffles are better."

prompt = prompt_with_function_information + user_prompt

llm_response(prompt)


# In[12]:


def clean_python_output(prompt: str):
    return prompt.replace("```python\n", "").replace("```", "")

clean_python_output(llm_response(prompt))


# In[13]:


output = clean_python_output(llm_response(prompt))

output


# Let's find a way to execute this code!

# In[14]:


exec(output)


# We connected LLM + FUNCTION via some simple PROMPT magic!

# Pancakes are undeniably better than waffles, RS! While some may argue that avocado waffles have a unique flavor, pancakes offer a fluffy, comforting texture that perfectly complements a variety of toppings, from fresh fruits to maple syrup. Their adaptability and classic appeal make them a quintessential breakfast choice that can satisfy any palate.
