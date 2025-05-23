import socket
import struct
import threading
import time
from plane_obj import Plane

UDP_IP = "0.0.0.0"  # listen on all interfaces
UDP_PORT = 49002    # default X-Plane UDP port

plane = Plane()

# UDP 設定
UDP_IP = "0.0.0.0"  # 綁定所有網卡，X-Plane 會主動傳送資料過來
UDP_PORT = 49002

# 有效的資料索引及對應名稱（可自定義補充）
INDEX_INFO = {
    3: "姿態 (Heading, Pitch, Roll)",
    13: "空速 (Indicated, True, Ground)",
    14: "垂直速度、角度 (VS, AOA, Slip)",
    17: "控制面位置 (Aileron, Elevator, Rudder)",
    20: "推力 (Throttle)",
    25: "GPS 位置 (Lat, Lon, Elev)",
    26: "GPS 速度與方向",
    34: "加速度",
    35: "磁羅盤 heading",
    37: "地形資訊",
    62: "油門與發動機狀態",
    116: "時間與 Frame Rate",
    121: "GPS 日期與時間"
}

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

def print_data_chunks(chunks):
    for index, values in chunks:
        desc = INDEX_INFO.get(index, "未知資料")
        print(f"\n📦 Index {index}: {desc}")
        for i, val in enumerate(values):
            print(f"  值[{i}] = {val:.3f}")


def onpen_udp_port(plane, lock):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    # print(f"✅ 等待來自 X-Plane 的 UDP 封包（port {UDP_PORT}）...")

    while True:
        data, addr = sock.recvfrom(4096)
        # print(f"\n📥 收到封包來自 {addr}")
        chunks = parse_xplane_data_packet(data)
        print_data_chunks(chunks)
        with lock:
            for index, values in chunks:
                plane.set_data(index, values)

if __name__ == "__main__":
    lock = threading.Lock()
    udp_thread = threading.Thread(target=onpen_udp_port, args=(plane, lock), daemon=True)
    udp_thread.start()

    while True:
        with lock:
            speed = plane.get_true_airspeed()
            if speed:
                print(f"Speed: {speed}")
            else:
                print("No Speed data available.")
            # 可加 sleep 避免洗版
        time.sleep(1)
