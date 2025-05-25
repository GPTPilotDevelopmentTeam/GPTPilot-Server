from queue import Queue
import socket
import time

class TCPServer:
    def __init__(self, host='127.0.0.1', port=87):
        self.host = host
        self.port = port
        self.server_socket = None
        self.message_queue = Queue()

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"Server started, listening on {self.host}:{self.port}")
        self.serve_forever()  # 直接在這裡呼叫

    def handle_client(self, conn, addr):
        print(f"Connection established with {addr}")
        while True:
            message = self.message_queue.get()
            if message is None:
                print("No message to send")
                continue
            print(f"Sending message to client: {message}")
            reply = ""
            message += '\0'
            try:
                conn.send(message.encode())
                reply = conn.recv(2048)
                if not reply:
                    print("Client disconnected.")
                    break
                time.sleep(1)
                reply_str = reply.decode('utf-8').strip('\0')
                print(f"Received from client: {reply_str}")
            except Exception as e:
                print(e)
                break
        conn.close()
        print("Connection closed.")

    def serve_forever(self):
        if self.server_socket is None:
            raise RuntimeError("Server not started. Call start_server() first.")
        try:
            while True:
                conn, addr = self.server_socket.accept()
                self.handle_client(conn, addr)
                time.sleep(1)
        except Exception as e:
            print(e)
        finally:
            self.server_socket.close()
            
    def send_message(self, message):
        """Send a message to the client."""
        self.message_queue.put(message)