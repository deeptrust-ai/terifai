#!/usr/bin/env python3

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get ELEVENLABS_API_KEY from environment variables
API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not API_KEY:
    print("Error: ELEVENLABS_API_KEY is not set in the .env file.")
    exit(1)

print(f"ELEVENLABS_API_KEY: {API_KEY}")


# Function to get all voices
def get_all_voices():
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("voices", [])
    else:
        print(f"Error getting voices: {response.status_code}")
        return []


# Function to delete a voice
def delete_voice(voice_id):
    url = f"https://api.elevenlabs.io/v1/voices/{voice_id}"
    headers = {"xi-api-key": API_KEY}
    response = requests.delete(url, headers=headers)
    print(response.json())
    return response.status_code, response.text


# Main execution
voices = get_all_voices()
print(f"Found {len(voices)} voices")

for voice in voices:
    voice_id = voice.get("voice_id")
    if voice_id:
        print(f"Deleting voice: {voice_id}")
        status_code, response_text = delete_voice(voice_id)
        print(f"Response: Status {status_code}, {response_text}")
    else:
        print(f"Skipping voice with no ID: {voice}")

print("All voices have been processed.")
