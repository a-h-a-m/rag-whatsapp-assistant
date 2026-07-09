import requests
import time


def download_audio(url):

    response = requests.get(url)

    response.raise_for_status()

    filename = f"voice_{int(time.time())}.oga"

    with open(filename, "wb") as file:
        file.write(response.content)

    return filename