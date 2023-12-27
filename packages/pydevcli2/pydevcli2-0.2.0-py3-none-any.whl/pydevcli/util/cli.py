"""Util CLI
"""
import typer
from rich.console import Console
from typing_extensions import Annotated

from .secrets import create_application_secret

app = typer.Typer()
console = Console()

@app.command()
def secret(
    nbytes: Annotated[int,  typer.Option(help="Number of bytes to generate")] = 32
):
    """
    Creates a new application secret.
    """
    console.print(create_application_secret(nb_bytes=nbytes))
