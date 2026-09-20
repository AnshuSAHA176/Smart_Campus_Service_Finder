
import os
import requests


ACCOUNT_ID = os.environ.get('ACCOUNT_ID')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')

def embedding_model(text: str) -> list[float]:
    """
    Generate a normalized embedding for the given text.
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")
    response = requests.post(
  f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/baai/bge-m3",
  headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
  json={"text": text}
)

   
    

    return response.json()['result']['data'][0]


def create_embedding(title: str, description: str,category:str) -> list[float]:
    """
    Create an embedding representing a place and its description and category.
    """

    text = (
        f"Place: {title.strip()}\n"
        f"Description: {description.strip()}"
        f"Category : {category}"
    )

    return embedding_model(text)







