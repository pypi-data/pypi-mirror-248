"""Main CLI to manage other scripts
"""
from typer import Typer

from .util.cli import app as util_app

app = Typer()
app.add_typer(util_app, name="util")

@app.command()
def hello(name: str):
    """Say hello NAME

    Args:
        name (str): _description_
    """
    print(f"Hello {name}")

if __name__ == "__main__":
    app()
