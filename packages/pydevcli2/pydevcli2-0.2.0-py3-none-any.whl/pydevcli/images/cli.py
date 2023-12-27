import typer
from rich.console import Console
from typing_extensions import Annotated

from .convert import convert_images_from_heic_to_jpeg, convert_batch_images_from_heic_to_jpeg

app = typer.Typer()
console = Console()

@app.command()
def convert_images(file: Annotated[str, typer.Argument(help="Filename or Directory for batch")] = ".", batch: Annotated[bool, typer.Option(help="Batch Convert")] = False):
    """Converts HEIC to JPEG
    """
    if batch:
        console.print("Batch Convert Directory")
        convert_images_from_heic_to_jpeg(file)

    else:
        console.print(f"Converting {file} to JPEG")
        convert_batch_images_from_heic_to_jpeg(file)
        