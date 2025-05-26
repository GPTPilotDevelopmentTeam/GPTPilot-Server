import threading

from .udp_server import onpen_udp_port

INFO = {
    1: ['real time', 'total time', 'mission time', 'timer', None, 'zulu time', 'local time', 'hobbs time'],
    3: [None] * 3 + ['speed'] + [None] * 4,
    13: ['trim_elev', 'trim_ailrn', 'trim_rudder', 'requested_flap', 'actual_flap', 'slat_ratio', 'requested_speedbrake', 'actual_speedbrake'],
    14: ['gear_status', 'wheel_brake'] + [None] * 6,
    17: ['Pitch', 'Roll', 'Heading'] + [None] * 5,
    20: ['latitude', 'longitude', 'altitude', 'gear altitude'] + [None] * 4,
    25: ['left requested throttle', 'right requested throttle'] + [None] * 6,
    26: ['left actual throttle', 'right actual throttle'] + [None] * 6,
    34: ['left engine power (hp)', 'right engine power (hp)'] + [None] * 6,
    35: ['left engine thrust (lb)', 'right engine thrust (lb)'] + [None] * 6,
    37: ['left engine RPM', 'right engine RPM'] + [None] * 6,
    62: ['left fuel weight', 'center fuel weight', 'right fuel weight'] + [None] * 5,
    117: ['audo_throttle', 'auto heading mode', 'auto altitude mode', None, 'bac', 'approaching', None, 'sync button'],
    118: ['ap airspeed', 'ap heading', 'ap vs', 'ap altitude'] + [None] * 4,
    121: ['APU is running', 'APU N1', 'APU rat', 'GPU rat', 'RAT rat', 'APU amp', 'GPU amp', 'RAT amp']
}

FLAP_VALUE = {
    0.0: 0,
    0.125: 1,
    0.25: 2,
    0.375: 5,
    0.5: 10,
    0.625: 15,
    0.75: 20,
    0.875: 30,
    1.0: 40
}

class Plane:
    def __init__(self):
        self.data = {}
        
        self._listening_thread = threading.Thread(target=onpen_udp_port, args=(self, threading.Lock()), daemon=True)
        self._listening_thread.start()

    def set_data(self, index, values):
        """設定某個 index 的資料（values 必須是 8 個 float 的 tuple/list）"""
        self.data[index] = list(values)

    def get_data(self, index):
        """取得某個 index 的資料（回傳 tuple of 8 floats，若無則回傳 8 個 0.0）"""
        return self.data.get(index, [0.0,] * 8)
    
    def __str__(self):
        str_list = []
        global INFO
        for k, v in self.data.items():
            if k not in INFO.keys():
                continue
            for i in range(8):
                if i < len(INFO[k]) and INFO[k][i] is not None:
                    if k == 13 and 'flap' in INFO[k][i]:
                        v[i] = FLAP_VALUE.get(v[i], v[i])
                    str_list.append(f'{INFO[k][i]}: {v[i]}\n')
                    
        return ''.join(str_list)