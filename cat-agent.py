# Leverage Your Agent’s Function Calling Capabilities
# In general, Language models can’t directly access external systems like databases, APIs, files, or even the terminal.
# However, some models have function calling capabilities which the agent can invoke to access external systems and data.

import requests
from pydantic_ai import Agent

agent = Agent(
    "google-gla:gemini-2.5-flash",
    instructions="Help users with cat breeds. Be precise. If you don't know the answer, say you don't know.",
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
    # url = f"https://api.thecatapi.com/v1/breeds/search?q={breed_name}"
    url = f"https://api.thecatapi.com/v1/breeds"
    response = requests.get(url)
    response.raise_for_status()
    if response.status_code == 200:
        data = response.json()
        if data:
            for breed in data:
                if breed["name"] == breed_name:
                    return breed
    return {"error": "Breed not found"}

result = agent.run_sync("Tell me about the Siamese cats.")
print(result.output)


# Alternative method to using the agent's tool decorator is pass it as argument during
# initialization. This is useful when you want to reuse tools across multiple agents.
# agent2 = Agent(
#     "google-gla:gemini-2.5-flash",
#     instructions="Help users with cat breeds. Be concise.",
#     tools=[find_breed_info]
# )