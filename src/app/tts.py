import requests
import tempfile
import os
import playsound

api_key = os.environ.get("OPENAI_API_KEY")
voice = "nova"  # alloy, echo, fable, onyx, nova, shimmer
model = "tts-1"

def text_to_speech(text):
    url = "https://api.openai.com/v1/audio/speech"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,
        "input": text,
        "voice": voice,
        "response_format": "mp3"
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print("Error:", response.text)
        return

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        tmpfile.write(response.content)
        tmpfile_path = tmpfile.name

    playsound.playsound(tmpfile_path)

    os.remove(tmpfile_path)

