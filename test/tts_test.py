import sys
import os

sys.path.insert(1, os.getcwd())

from src.app import tts

tts.start()


while True:
    text = input("Enter text to convert to speech (or 'exit' to quit): ")
    if text.lower() == 'exit':
        break
    tts.interrupt()
    tts.text_to_speech(text)