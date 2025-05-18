from app import stt, tts
from engine import StreamInteractionModel, ActionDeterminationModel
import time

model = StreamInteractionModel()
action = ActionDeterminationModel()

def callback(text):
    global model
    print(f'User says: {text}')
    gen = model.send_message(text)
    tts.interrupt()
    
    for g in gen:
        print(f'processing: {g}')
        action.analyzing_message(g)
        tts.text_to_speech(g)
    
stt.set_transcription_callback(callback)
stt.start()
tts.start()

while True:
    time.sleep(1)