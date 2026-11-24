# Leverage Your Agent’s Function Calling Capabilities
# In general, Language models can’t directly access external systems like databases, APIs, files, or even the terminal.
# However, some models have function calling capabilities which the agent can invoke to access external systems and data.

import os

import requests
from pydantic_ai import Agent, capture_run_messages
from pydantic_ai.messages import (
    ModelRequest, ModelResponse,
    ToolCallPart, ToolReturnPart, TextPart,
)


agent = Agent(
    "google-gla:gemini-2.5-flash",
    # instructions="Help users with cat breeds, including obtaining a list of available breeds. Be precise. If you don't know the answer, say you don't know.",
    system_prompt="""
        You are a helpful cat expert.

        When the user asks for cat breeds:
        - use the get_cat_breeds tool
        - do not invent breed names

        When discussing cats:
        - provide concise answers
        - include breed origin when available

        If a tool call fails:
        - explain the error
        - suggest a retry
    """
)

# This decorator registers the function as a tool that the agent can call.
# The agent/LLM will choose which tools to call based on the query and the docstrings.
# Use @agent.tool when your tool needs access to the run context,
# and @agent.tool_plain when it doesn’t.
@agent.tool_plain
def find_breed_info(breed_name: str) -> dict:
    # The following docstring is important. It tells the agent what it does so it knows when
    # to use it.
    """Find information about a cat breed using TheCatAPI."""
    url = f"https://api.thecatapi.com/v1/breeds/search?q={breed_name}"
    # url = f"https://api.thecatapi.com/v1/breeds"
    headers = {
    "x-api-key": os.environ["CAT_API_KEY"]
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    if response.status_code == 200:
        data = response.json()
        if data:
            for breed in data:
                if breed["name"] == breed_name:
                    return breed
    return {"error": "Breed not found"}

@agent.tool_plain
def get_cat_breeds() -> list[str]:
    """Get a list of cat breeds using TheCatAPI."""
    url = "https://api.thecatapi.com/v1/breeds"
    headers = {
        "x-api-key": os.environ["CAT_API_KEY"]
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    if response.status_code == 200:
        data = response.json()
        return [breed["name"] for breed in data]
    return []


# Alternative method to using the agent's tool decorator is pass it as argument during
# initialization. This is useful when you want to reuse tools across multiple agents.
# agent2 = Agent(
#     "google-gla:gemini-2.5-flash",
#     instructions="Help users with cat breeds. Be concise.",
#     tools=[find_breed_info]
# )


def tool_calls(result):
    return [
        (p.tool_name, p.args)
        for m in result.new_messages()
            for p in m.parts
                if isinstance(p, ToolCallPart)
    ]

if __name__ == "__main__":
    # Run the agent in a loop to allow multiple queries.
    while True:
        query = input("Ask me about cat breeds (or type 'exit' to quit): ")
        if query.lower() == "exit":
            break
        with capture_run_messages() as messages:
            try:
                result = agent.run_sync(query)
                print(result.output)
                calls = tool_calls(result)
                if calls:
                    print("Tool calls made during this run:")
                    for tool_name, args in calls:
                        print(f"  Tool: {tool_name}, Args: {args}")
            except Exception as err:
                print(err)
