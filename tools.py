import os
import requests

BASE_URL = "https://api.thecatapi.com/v1"

def find_breed_info(breed_name: str) -> dict:
  # The following docstring is important. It tells the agent what it does so it knows when
  # to use it.
  """Find information about a cat breed using TheCatAPI."""

  headers = {
  "x-api-key": os.environ["CAT_API_KEY"]
  }
  response = requests.get(
    f"{BASE_URL}/breeds/search",
    params={"q": breed_name},
    headers=headers,
    timeout=10)
  
  response.raise_for_status()
  if response.status_code == 200:
      data = response.json()
      if data:
          for breed in data:
              if breed["name"] == breed_name:
                  return breed
  return {"error": "Breed not found"}

  # return response.json()

def get_cat_breeds() -> list[str]:
  """Get a list of cat breeds using TheCatAPI."""

  headers = {
  "x-api-key": os.environ["CAT_API_KEY"]
  }
  response = requests.get(
    f"{BASE_URL}/breeds",
    headers=headers,
    timeout=10)

  response.raise_for_status()
  if response.status_code == 200:
      data = response.json()
      return [breed["name"] for breed in data]
  return []