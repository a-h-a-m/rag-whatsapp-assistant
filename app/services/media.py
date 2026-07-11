import time
from pathlib import Path

import requests


def download_audio(url):
    
    media_dir = Path("media")
    media_dir.mkdir(exist_ok=True)

    response = requests.get(url)

    response.raise_for_status()

    filename = media_dir / f"voice_{int(time.time())}.oga"

    with open(filename, "wb") as file:
        file.write(response.content)

    return filename
