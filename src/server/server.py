import socket
import time

def start_server(host='127.0.0.1', port=87):
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 允許重複綁定
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server started, listening on {host}:{port}")

def handle_client(conn, addr):
    print(f"Connection established with {addr}")
    while True:
        message = "hi"
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

if __name__ == '__main__':
    start_server()
    while True:
        try:
            conn, addr = server_socket.accept()
            handle_client(conn, addr)
        except Exception as e:
            print(e)
            break
    server_socket.close()