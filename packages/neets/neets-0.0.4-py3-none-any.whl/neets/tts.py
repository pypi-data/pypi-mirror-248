import requests
import os
import uuid
from rich.console import Console
from rich.table import Table
from rich.spinner import Spinner
from rich.live import Live

def get_tts(voice, text, output_fmt="wav", output_file=None): 

    console = Console()
    url = "https://api.neets.ai/v1/tts"

    api_key = os.getenv('NEETS_API_KEY')

    headers = {
        "Authorization": "Bearer " + api_key, 
        'X-API-Key': api_key
    }
    params = {
        'voice_id': voice,
        'text': text,
        'fmt': output_fmt 
    }

    with Live(Spinner("dots", text="Fetching audio...", style="bold green"), console=console, auto_refresh=True):
        response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        console.print(f"Error: {response.status_code}")
        return None

    if output_file == None:
        output_file = f'{voice}_{str(uuid.uuid1())}.{output_fmt}'

    if response.status_code == 200:
        with open(f"{output_file}", 'wb') as file:
            file.write(response.content)
        console.print(f"Saved audio to [yellow]{output_file}[/yellow]")
    else:
        console.print(f"Error: {response.status_code}")


def get_or_print_voices(voice):
    console = Console()
    voices = get_voices()

    if voice in voices:
        return voice 
    else:
        print_voices()
        error_str = f"[red]Invalid voice:[/red] [bold]{voice}[/bold]\nPlease select a voice from the list above."
        console.print(error_str)
        return None


def print_voices():
    console = Console()
    voices = get_voices()
    # make pretty table to display voices
    voices_iter = iter(voices)
    table = Table(show_header=False, header_style="bold magenta")
    for _ in range(4): 
        table.add_column(justify="left")

    while True:
        row = []
        for _ in range(4):  
            try:
                row.append(next(voices_iter))
            except StopIteration:
                break
        if not row:
            break
        while len(row) < 4:
            row.append("")
        table.add_row(*row)

    console.print(table)


def get_voices():
    voices = [
        'angie', 'william', 'donald-trump', 'ben-shapiro', 'mark-zuckerberg', 'tucker-carlson', 'alex-jones', 'aoc', 
        'barack-obama', 'andrew-yang', 'kamala-harris', 'andrew-tate', 'lex-fridman', 'elon-musk', '50-cent', 
        'anderson-cooper', 'angela-merkel', 'anthony-fauci', 'antonio-banderas', 'ariana-grande', 'arnold-schwarzenegger', 
        'barry-white', 'ben-affleck', 'bernie-sanders', 'beyonce', 'bill-clinton', 'dj-khaled', 'tupac', 'will-smith', 
        'bill-oreilly', 'billie-eilish', 'cardi-b', 'casey-affleck', 'conor-mcgregor', 'darth-vader', 'dr-dre', 'dr-phil', 
        'drake', 'elizabeth-holmes', 'emma-watson', 'gilbert-gottfried', 'greta-thunberg', 'grimes', 'hillary-clinton', 
        'jason-alexander', 'jay-z', 'jeff-bezos', 'joe-rogan', 'john-cena', 'jordan-peterson', 'justin-trudeau', 'kanye-west', 
        'kermit', 'lil-wayne', 'matt-damon', 'mike-tyson', 'morgan-freeman', 'patrick-stewart', 'paul-mccartney', 'pokimane', 
        'rachel-maddow', 'ron-desantis', 'sam-altman', 'sbf', 'scarlett-johansson', 'sean-hannity', 'snoop-dogg', 'stephen-hawking', 
        'warren-buffett', 'taylor-swift'
    ]
    return voices
