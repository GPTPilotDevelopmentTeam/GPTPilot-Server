from app import stt, tts
from engine import StreamInteractionModel
import time

model = StreamInteractionModel()

def callback(text):
    global model
    print(f'User says: {text}')
    gen = model.send_message(text)
    
    for g in gen:
        print(f'processing: {g}')
        tts.text_to_speech(g)
    
    
stt.set_transcription_callback(callback)
stt.start()

while True:
    time.sleep(1)