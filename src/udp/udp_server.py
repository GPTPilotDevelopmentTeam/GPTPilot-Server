import socket
import struct
import threading
import time
from plane_obj import Plane

UDP_IP = "0.0.0.0"  # listen on all interfaces
UDP_PORT = 49002    # default X-Plane UDP port

plane = Plane()

def parse_xplane_data_packet(packet: bytes):
    """解析 X-Plane UDP 封包，回傳 list of (index, [floats])"""
    if not packet.startswith(b'DATA*'):
        print("⚠️ 非 DATA* 封包，略過")
        return []

    payload = packet[5:]  # 移除 header
    chunks = []

    for i in range(0, len(payload), 36):  # 每 36 bytes 是一組
        block = payload[i:i+36]
        if len(block) < 36:
            print("⚠️ 封包長度錯誤，略過")
            continue

        index = int.from_bytes(block[:4], byteorder='little')
        values = struct.unpack('<8f', block[4:])  # 小端 8 個 float

        chunks.append((index, values))
    
    return chunks

def onpen_udp_port(plane, lock):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(4096)
        chunks = parse_xplane_data_packet(data)
        #print_data_chunks(chunks)
        with lock:
            for index, values in chunks:
                plane.set_data(index, values)

if __name__ == "__main__":
    lock = threading.Lock()
    udp_thread = threading.Thread(target=onpen_udp_port, args=(plane, lock), daemon=True)
    udp_thread.start()

    while True:
        print(plane)
        time.sleep(1)
