import threading
import time
import os
import sys
from .tcp.tcp_server import TCPServer

class Server:
    def __init__(self):
        self.tcp_thread = None
       
    def run_tcp_server(self):
        self.server = TCPServer()
        self.tcp_thread = threading.Thread(target=lambda: self.server.start_server(), daemon=True)
        self.tcp_thread.start()
        print("TCP server is running in a separate thread.")
    
    def send_message(self, message):
        """Send a message to the TCP server."""
        if self.tcp_thread is not None:
            self.server.send_message(message)
        else:
            print("TCP server is not running. Cannot send message.")
