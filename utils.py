import os
import openai
import pandas as pd
from pathlib import Path

os.environ['OPENAI_API_KEY'] = "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"
openai.api_key = "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"


def ask_openai(
        # we tell the model to answer our question using the results from the query_message as source of information
        query: str,
        model: str = "gpt-3.5-turbo",
        # token_budget: int = 4096 - 500,
        print_message: bool = False,
        prompt: str = ""
) -> str:
    """Answers a query using GPT and a dataframe of relevant texts and embeddings."""
    messages = [
        {"role": "system", "content": f"""
        You are a German AI assistant. 
        {prompt}"""},
        {"role": "user", "content": query},
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0
    )
    print(prompt)
    response_message = response["choices"][0]["message"]["content"]
    return response_message