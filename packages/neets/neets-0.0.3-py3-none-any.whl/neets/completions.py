import requests
import os 

from rich.console import Console
from rich.markdown import Markdown


def get_completion(prompt, instructions="", model="Neets-7B", max_tokens=500):

    console = Console()

    url = "https://api.neets.ai/v1/chat/completions"

    api_key = os.getenv('NEETS_API_KEY')

    headers = {
        'X-API-Key': api_key, 
        "Authorization": "Bearer " + api_key, 
        'Content-Type': 'application/json'
    }

    data = {
        "messages": [
            {
                "content": f"{instructions}: {prompt}",
                "role": "user"
            }
        ],
        "model": model, 
        "frequency_penalty": 0,
        "max_tokens": max_tokens,
        "n": 1,
        "presence_penalty": 0,
        "response_format": {
            "type": "json_object"
        },
        "seed": -9223372036854776000,
        "stop": "null",
        "stream": "false",
        "temperature": 1,
        "top_p": 1
        }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code != 200:
        console.print(f"Error: {response.status_code}")
        return None

    if response.text:  
        res = response.json()
    else:
        console.print("Empty response received")
        res = None

    res_str = res['choices'][0]['message']['content']
    console.print(Markdown(res_str))


