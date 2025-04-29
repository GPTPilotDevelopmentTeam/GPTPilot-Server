import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

from src.engine import InteractionModel
from src.app.tts import text_to_speech

model = InteractionModel()
while True:
    s = input()
    talk, cmd = model.send_message(s)
    print(f"Talk: {talk}")
    print(f"Command: {cmd}")
    text_to_speech(talk)