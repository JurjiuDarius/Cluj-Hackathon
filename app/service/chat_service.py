import os

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

AZURE_ENDPOINT = os.environ.get("AZURE_ENDPOINT")
AZURE_API_KEY = os.environ.get("AZURE_API_KEY")
PROMPT_BEGINNING = "I am looking at my pet's medical history. Please explain to me the following terms: "

client = AzureOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_API_KEY,
    api_version="2024-02-01",
)


def get_completion_for_text(data):
    prompt_text = PROMPT_BEGINNING + data["text"]
    completion = client.chat.completions.create(
        model="FirstDeployment",
        messages=[
            {
                "role": "user",
                "content": prompt_text,
            },
        ],
    )

    return completion.choices[0].message.content, 200
