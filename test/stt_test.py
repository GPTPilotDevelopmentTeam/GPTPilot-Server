import sys
import os
sys.path.insert(1, os.getcwd())

from src.app import stt

import time

stt.start()
s = 0
while True:
    time.sleep(1)