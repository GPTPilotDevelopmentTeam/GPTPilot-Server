import tkinter as tk
from tkinter import ttk
import os
import sys

sys.path.insert(1, os.getcwd())
from src.app import stt

# UI 資料狀態
stt_state = {
    "text": "",
    "record_sec": 0.0,
    "silence_sec": 0.0,
    "volume": 0.0,
    "threshold": 0.0,
    "silence_limit": 1.0,
    "max_duration": 5.0
}

# UI 顯示變數
stt_text = tk.StringVar(value="")
stt_volume = tk.DoubleVar(value=0.0)
stt_volume_label = tk.StringVar(value="0.00")

stt_threshold_display = tk.StringVar(value="Threshold: 0.00")
stt_silence_display = tk.StringVar(value="Silence: 0.0 / 1.0 secs")
stt_max_duration_display = tk.StringVar(value="Recording: 0.0 / 5.0 secs")

def open_stt_settings():
    settings_win = tk.Toplevel()
    settings_win.title("STT Settings")
    settings_win.geometry("320x250")

    # Threshold Slider
    tk.Label(settings_win, text="Threshold").pack()
    threshold_var = tk.DoubleVar(value=stt_state["threshold"])
    threshold_slider = tk.Scale(settings_win, from_=0.01, to=1.0, resolution=0.01, orient="horizontal", variable=threshold_var)
    threshold_slider.pack(fill="x", padx=10)

    # Silence Duration Slider
    tk.Label(settings_win, text="Silence Duration (sec)").pack()
    silence_var = tk.DoubleVar(value=stt_state["silence_limit"])
    silence_slider = tk.Scale(settings_win, from_=0.0, to=3.0, resolution=0.1, orient="horizontal", variable=silence_var)
    silence_slider.pack(fill="x", padx=10)

    # Max Record Duration Slider
    tk.Label(settings_win, text="Max Record Duration (sec)").pack()
    record_var = tk.DoubleVar(value=stt_state["max_duration"])
    record_slider = tk.Scale(settings_win, from_=1.0, to=10.0, resolution=0.5, orient="horizontal", variable=record_var)
    record_slider.pack(fill="x", padx=10)

    def save_settings():
        stt.THRESHOLD = threshold_var.get()
        stt.SLIENCE_DURATION = silence_var.get()
        stt.MAX_RECORDING_DURATION = record_var.get()
        update_stt_status(
            threshold=threshold_var.get(),
            silence_limit=silence_var.get(),
            max_duration=record_var.get()
        )
        settings_win.destroy()

    tk.Button(settings_win, text="Save", command=save_settings).pack(pady=10)

def create_stt_frame(parent):
    stt_frame = ttk.LabelFrame(parent, text="🎙️ Speech-to-Text")
    stt_frame.pack(fill="x", padx=5, pady=5)

    # 辨識文字
    ttk.Label(stt_frame, text="辨識文字:").pack(anchor="w", padx=5, pady=2)
    stt_text_label = ttk.Label(stt_frame, textvariable=stt_text, background="white", anchor="w")
    stt_text_label.pack(fill="x", padx=5)

    # 音量條
    volume_frame = ttk.Frame(stt_frame)
    volume_frame.pack(fill="x", padx=5, pady=(0, 5))
    
    ttk.Label(volume_frame, textvariable=stt_threshold_display).pack(side="left", padx=(0, 5))
    volume_bar = ttk.Progressbar(volume_frame, variable=stt_volume, maximum=1.0)
    volume_bar.pack(side="left", fill="x", expand=True, padx=5)
    ttk.Label(volume_frame, text="1.0").pack(side="left", padx=(5, 0))

    # 條下方顯示音量值
    ttk.Label(stt_frame, textvariable=stt_volume_label, anchor="center").pack(fill="x", padx=10, pady=(2, 5))

    # 參數顯示
    param_frame = ttk.Frame(stt_frame)
    param_frame.pack(fill="x", padx=5, pady=(0, 5))
    ttk.Label(param_frame, textvariable=stt_silence_display).pack(anchor="w")
    ttk.Label(param_frame, textvariable=stt_max_duration_display).pack(anchor="w")

    # 設定按鈕
    ttk.Button(stt_frame, text="Settings", command=open_stt_settings).pack(anchor="e", padx=5, pady=(0, 5))

def update_stt_status(
    text=None,
    record_sec=None,
    silence_sec=None,
    volume=None,
    threshold=None,
    silence_limit=None,
    max_duration=None
):
    if text is not None:
        stt_state["text"] = text

    if record_sec is not None:
        stt_state["record_sec"] = record_sec

    if silence_sec is not None:
        stt_state["silence_sec"] = silence_sec

    if volume is not None:
        stt_state["volume"] = volume

    if threshold is not None:
        stt_state["threshold"] = threshold

    if silence_limit is not None:
        stt_state["silence_limit"] = silence_limit

    if max_duration is not None:
        stt_state["max_duration"] = max_duration

    
def _update_stt_ui():
    stt_text.set(stt_state["text"])
    stt_volume.set((stt_state["volume"] - stt_state["threshold"]) / (1.0 - stt_state["threshold"]))
    stt_volume_label.set(f"{stt_state['volume']:.2f}")
    stt_threshold_display.set(f"Threshold: {stt_state['threshold']:.2f}")
    stt_silence_display.set(f"Silence: {stt_state['silence_sec']:.1f} / {stt_state['silence_limit']:.1f} secs")
    stt_max_duration_display.set(f"Recording: {stt_state['record_sec']:.1f} / {stt_state['max_duration']:.1f} secs")
