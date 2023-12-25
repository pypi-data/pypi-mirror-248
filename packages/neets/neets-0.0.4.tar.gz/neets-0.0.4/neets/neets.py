import click

from neets.completions import get_completion 
from neets.tts import get_tts, get_or_print_voices, print_voices
from neets.utils import check_api_key

NEETS_API_CLI_VERSION = "0.0.4"

@click.group()
@click.version_option(NEETS_API_CLI_VERSION, message='Neets api cli version: %(version)s')
def cli():
    pass


@cli.command(help="Send a prompt to the neets.ai API and print a completion.") 
@click.option('--prompt', '-p', help='The prompt to use for the model.', required=True)
@click.option('--model', '-m', help='The model to use for the completion.', default="Neets-7B")
@click.option('--max-tokens', '-mt', help='The maximum number of tokens to generate.', default=500)  
@click.option('--quiet', '-q', help="Don't show progress spinner", is_flag=True)
def chat(prompt, model, max_tokens, quiet):

    has_api_key = check_api_key()
    if not has_api_key:
        return

    get_completion(prompt, model, max_tokens, quiet)


@cli.command(help="Convert text to speech using a voice from the neets.ai API.")
@click.option('--voice', '-v', help='The voice to use for the tts.', required=True)
@click.option('--text', '-t', help='The text to use for the tts.', required=True)
@click.option('--output-fmt', '-f', help='The output format for the tts.', default="wav")
@click.option('--output-file', '-o', help='The output file for the tts.', default=None)
def tts(voice, text, output_fmt, output_file):

    has_api_key = check_api_key()
    if not has_api_key:
        return

    voice = get_or_print_voices(voice)
    if voice == None:
        return
    
    get_tts(voice, text, output_fmt, output_file)


@cli.command(help="Print a list of available voices from the neets.ai API.")
def voices():
    print_voices()