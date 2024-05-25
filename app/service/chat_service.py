import os

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI

AZURE_ENDPOINT = os.environ.get("AZURE_ENDPOINT")
AZURE_API_KEY = os.environ.get("AZURE_API_KEY")

client = AzureOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=AZURE_API_KEY,
    api_version="2024-02-01",
)
