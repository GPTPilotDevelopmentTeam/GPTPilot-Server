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

class Plane:
    def __init__(self):
        self.data = {}

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
                    str_list.append(f'{INFO[k][i]}: {v[i]}\n')
                    
        return ''.join(str_list)

    # --- Index 3: 姿態 (Heading, Pitch, Roll) ---
    def get_heading(self): return self.get_data(3)[0]
    def get_pitch(self): return self.get_data(3)[1]
    def get_roll(self): return self.get_data(3)[2]

    # --- Index 13: 速度 ---
    def get_airspeed(self): return self.get_data(13)[0]
    def get_true_airspeed(self): return self.get_data(13)[1]
    def get_groundspeed(self): return self.get_data(13)[2]

    # --- Index 14: 垂直速度與角度 ---
    def get_vertical_speed(self): return self.get_data(14)[0]
    def get_aoa(self): return self.get_data(14)[3]  # Angle of Attack
    def get_slip_angle(self): return self.get_data(14)[4]

    # --- Index 17: 控制面 ---
    def get_aileron(self): return self.get_data(17)[0]
    def get_elevator(self): return self.get_data(17)[1]
    def get_rudder(self): return self.get_data(17)[2]

    # --- Index 20: 推力 ---
    def get_thrust(self): return self.get_data(20)[0]

    # --- Index 25: GPS 位置 ---
    def get_latitude(self): return self.get_data(25)[0]
    def get_longitude(self): return self.get_data(25)[1]
    def get_elevation(self): return self.get_data(25)[2]

    # --- Index 26: GPS 速度與方向 ---
    def get_gps_speed(self): return self.get_data(26)[0]
    def get_gps_heading(self): return self.get_data(26)[1]

    # --- Index 34: 加速度 ---
    def get_accel_x(self): return self.get_data(34)[0]
    def get_accel_y(self): return self.get_data(34)[1]
    def get_accel_z(self): return self.get_data(34)[2]

    # --- Index 35: 羅盤資訊 ---
    def get_mag_heading(self): return self.get_data(35)[0]

    # --- Index 37: 地形資訊 ---
    def get_agl(self): return self.get_data(37)[1]  # Above Ground Level

    # --- Index 62: 油門與狀態 ---
    def get_throttle_ratio(self): return self.get_data(62)[0]
    def get_engine_running(self): return self.get_data(62)[7]  # 1=running, 0=off

    # --- Index 116: 時間資訊 ---
    def get_elapsed_time_sec(self): return self.get_data(116)[0]
    def get_frame_rate(self): return self.get_data(116)[2]

    # --- Index 121: GPS 日期與時間 ---
    def get_gps_time(self): return self.get_data(121)[0]
    def get_gps_date(self): return self.get_data(121)[1]