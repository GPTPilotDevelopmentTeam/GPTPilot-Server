import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

from src.engine import StreamInteractionModel
from threading import Thread
from queue import Queue

q = Queue()

def _():
    while True:
        if not q.empty():
            s = q.get()
            for i in s:
                print(i)

Thread(target=_, daemon=True).start()
model = StreamInteractionModel()
while True:
    s = input()
    stream = model.send_message(s)
    q.put(stream)