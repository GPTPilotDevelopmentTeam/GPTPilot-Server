from app import stt, tts
from engine import InteractionModel

def callback(text):
    """Callback function to handle the transcribed text."""
    global model
    print(f"Transcribed text: {text}")
    talk, cmd = model.send_message(text)
    print(talk)
    
    
model = InteractionModel()
stt.set_transcription_callback(callback)
stt.start()

import time

while True:
    time.sleep(1)
