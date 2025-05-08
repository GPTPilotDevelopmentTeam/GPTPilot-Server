import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

from src.engine import StreamInteractionModel
from src.app.tts_engine.openai_tts import text_to_speech

model = StreamInteractionModel()
while True:
    s = input()
    stream = model.send_message(s)
    for s in stream:
        print(s)
        print('[next]')