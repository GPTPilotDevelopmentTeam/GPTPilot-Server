from openai import OpenAI
import requests
import tempfile
import os

client = OpenAI()

def text_to_speech(texts: str, instructions: str=''):
    global client
    with client.audio.speech.with_streaming_response.create(
        model='gpt-4o-mini-tts',
        voice='nova',
        input=texts,
        instructions=instructions
    ) as response:
        if response.status_code != 200:
            print("Error:", response.text)
            return

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            response.stream_to_file(tmpfile.name)
            tmpfile_path = tmpfile.name

        return tmpfile_path
   