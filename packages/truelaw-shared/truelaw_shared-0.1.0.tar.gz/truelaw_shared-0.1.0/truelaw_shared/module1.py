import openai
import time
from openai import AzureOpenAI

def chat_completion(message_text, model_name, credentials):
    MAX_RETRIES = 5
    BACKOFF_FACTOR = 2

    for attempt in range(MAX_RETRIES):
        try:
            response_content = None

            if model_name == 'mixtral':
                client = openai.OpenAI(
                    base_url="https://api.endpoints.anyscale.com/v1",
                    api_key=credentials['mixtral_api_key']
                )
                chat_completion = client.chat.completions.create(
                    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                    messages=message_text,
                    temperature=0.7
                )
                response_content = chat_completion.choices[0].message.content

            elif model_name == 'azure_openai':
                client = AzureOpenAI(
                    azure_endpoint="https://broccoli-gpt.openai.azure.com/",
                    api_key=credentials['azure_api_key'],
                    api_version="2023-05-15"
                )
                response = client.chat.completions.create(
                    model="gpt-4-32k",
                    messages=message_text,
                )
                response_content = response.choices[0].message.content

            if response_content is not None:
                return response_content
            else:
                raise ValueError("No response content")

        except ValueError as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(BACKOFF_FACTOR ** attempt)
            else:
                raise e


