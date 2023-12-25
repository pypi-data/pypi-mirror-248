import requests
import os 

from rich.console import Console
from rich.markdown import Markdown
from rich.spinner import Spinner
from rich.live import Live

def get_completion(prompt, model="Neets-7B", max_tokens=500, quiet=False):

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
                "content": f"{prompt}",
                "role": "user"
            }
        ],
        "response_format": {
            "type": "json_object"
        },
        "model": model, 
        "max_tokens": max_tokens,
        "frequency_penalty": 0,
        "n": 1,
        "presence_penalty": 0,
        "seed": -9223372036854776000,
        "stop": "null",
        "stream": "false",
        "temperature": 1,
        "top_p": 1
        }

    if not quiet:
        with Live(Spinner("simpleDots", style="bold green"), console=console, auto_refresh=True):
            response = requests.post(url, json=data, headers=headers)
    else:
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


