from pydantic import BaseModel
from typing import Literal
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()
print(os.environ.get('GROQ_API_KEY'))
client=Groq(api_key=os.environ.get('GROQ_API_KEY'))


class SearchIntent(BaseModel):
    category: Literal[
        "academic",
        "administration",
        "culture",
        "environment",
        "food",
        "health",
        "hostel",
        "laboratory",
        "library",
        "parking",
        "research",
        "security",
        "sports",
        "student_services",
        "technology",
        "utilities",
        "unknown",
    ]


def extract_search_intent(message: str):

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": """
You classify campus search queries.

Return the result as valid JSON.

Choose exactly one category:

academic
administration
culture
environment
food
health
hostel
laboratory
library
parking
research
security
sports
student_services
technology
utilities
unknown

If the query does not clearly indicate a category,
return "unknown".

The JSON response must have this format:

{
    "category": "library"
}
"""
            },
            {
                "role": "user",
                "content": message
            }
        ],
        response_format={
            "type": "json_object"
        }
    )

    return SearchIntent.model_validate_json(
        response.choices[0].message.content
    )