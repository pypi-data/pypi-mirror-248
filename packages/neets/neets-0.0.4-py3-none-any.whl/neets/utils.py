import os
import datetime
import csv
from rich.console import Console

def check_api_key():
    console = Console()
    api_key = os.getenv('NEETS_API_KEY')

    if api_key == None:
        console.print("\n[red]Error:[/red] No API key found. Set your API key using:")
        console.print("\n\t[bold]export NEETS_API_KEY=[/bold][yellow]your-api-key[/yellow]")
        console.print("\nYou can find your API key at [link=https://neets.ai]https://neets.ai[/link]\n")
        return False

    return True


def log_tts(output_file, voice, text):
    text = text.replace('\n', ' ')

    if not os.path.exists('logs'):
        os.makedirs('logs')

    with open('logs/tts_log.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([output_file, datetime.datetime.now(), voice, text])



def prompt_res_logger(prompt, res):
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    with open('logs/prompt_res.csv', 'a') as file:
        writer = csv.writer(file)
        model_res = res['choices'][0]['message']['content'].strip("\n")
        writer.writerow([datetime.datetime.now(), prompt, model_res, res])

