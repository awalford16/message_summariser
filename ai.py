import openai

import openai
import os


class OpenAI:
    def __init__(self):
        # Set up OpenAI API credentials
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def summarize(self, message_source, topic):
        # Set up the prompt for the summarization task
        with open(f"{message_source}_{topic}.txt", "r") as f:
            text = f.read()

        prompt = f"Please summarize the following text:\n{text}"

        # Set up OpenAI API request parameters
        model_engine = "text-davinci-002"
        params = {
            "engine": model_engine,
            "prompt": prompt,
            "temperature": 0.5,
            "max_tokens": 10,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
        }

        # Call the OpenAI API to generate a summary
        response = openai.Completion.create(**params)

        # Extract the summary from the OpenAI API response
        return response.choices[0].text.strip()
