import os
from subprocess import Popen, PIPE
from rich.console import Console

console = Console()

def convert_images_from_heic_to_jpeg(filename: str):
    """Converts HEIC to JPEG
    """
    console.print(f"Converts HEIC to JPEG file {filename}")

def convert_batch_images_from_heic_to_jpeg(directory_path: str):
    """Converts HEIC to JPEG in batch
    """
    console.print(f"Converts HEIC to JPEG in directory {directory_path}")
    command = ["magick", "convert", "input.heic", "output.jpeg"]
    files = os.listdir(directory_path)

    for filename in files:
        if os.path.isfile(os.path.join(directory_path, filename)):
            file_extension = os.path.splitext(filename)[-1]  # Remove the leading dot
            file_basename = filename[:-len(file_extension)]
            if file_extension.lower() != ".heic":
                continue
            command[2] = os.path.join(directory_path, file_basename+file_extension)
            command[3] = os.path.join(directory_path, file_basename+".jpeg")
            console.print(f"Converting {filename} to JPEG")
            process = Popen(command, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            console.print(stdout)
            console.print(stderr)
            if process.returncode != 0:
                console.print(f"Failed converting {filename} to JPEG")
            else:
                console.print(f"Successfully converted {filename} to JPEG")


if __name__ == "__main__":
    convert_batch_images_from_heic_to_jpeg("/Users/giraycoskun/Code/Temp")