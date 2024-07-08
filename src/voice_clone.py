import os
import uuid
from io import BytesIO

import requests
from dotenv import load_dotenv
from modal import App, Image

load_dotenv()

image = (
    Image.debian_slim()
    .pip_install("requests", "python-dotenv")
    .env({"ELEVENLABS_API_KEY": os.getenv("ELEVENLABS_API_KEY")})
)
app = App("terifai-functions", image=image)


@app.function()
def add_elevenlabs_voice(audio: bytes):
    url = "https://api.elevenlabs.io/v1/voices/add"
    api_key = os.getenv("ELEVENLABS_API_KEY")

    # Use BytesIO to simulate a file
    audio_file = BytesIO(audio)
    filename = f"audio_{uuid.uuid4().hex[:8]}.wav"

    files = {"files": (filename, audio_file, "audio/wav")}

    data = {
        "name": f"terifai-{uuid.uuid4().hex[:8]}",
        "description": "Voice added from terifai service.",
    }

    headers = {"xi-api-key": api_key}

    response = requests.post(url, files=files, data=data, headers=headers)

    response.raise_for_status()  # Raises an HTTPError for bad responses

    voice_id = response.json()["voice_id"]

    print(f"Voice cloning successful: {voice_id}")

    return voice_id
