import threading
import time
import os
import sys
from .tcp.tcp_server import TCPServer

class Server:
    def __init__(self):
        self.tcp_thread = None
       
    def run_tcp_server(self):
        self.tcp_thread = threading.Thread(target=lambda: TCPServer().start_server(), daemon=True)
        self.tcp_thread.start()
        print("TCP server is running in a separate thread.")
