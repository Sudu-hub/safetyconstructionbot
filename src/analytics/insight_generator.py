from openai import AzureOpenAI
from config import (
    AZURE_OPENAI_KEY,
    AZURE_ENDPOINT,
    AZURE_API_VERSION,
    AZURE_CHAT_DEPLOYMENT
)

client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    api_version=AZURE_API_VERSION
)


def generate_safety_insight(question, analytics_result):

    messages = [
        {
            "role": "system",
            "content": "You are a construction safety AI advisor."
        },
        {
            "role": "user",
            "content": f"""
Question:
{question}

Analytics Result:
{analytics_result}

Explain the result and give practical safety recommendations.
"""
        }
    ]

    response = client.chat.completions.create(
        model=AZURE_CHAT_DEPLOYMENT,
        messages=messages,
        temperature=0.3
    )

    return response.choices[0].message.content