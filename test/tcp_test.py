import sys
import os

sys.path.insert(1, os.getcwd())
from src.server import Server

from threading import Thread

test= Server()
test.run_tcp_server()

import time

time.sleep(1)
for i in range(10):
    print(i)
    test.send_message(f"Test message {i}")
    time.sleep(1)