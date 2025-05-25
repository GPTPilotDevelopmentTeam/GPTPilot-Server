import tkinter as tk
from tkinter import ttk
from queue import Queue
import os
import sys

root = tk.Tk()
root.title("GPTPilot Monitor")
root.geometry("800x600")
root.configure(bg="#f0f0f0")

sys.path.insert(1, os.getcwd())
from src.ui.stt_ui import create_stt_frame, update_stt_status, _update_stt_ui
from src.ui.interaction_ui import create_interaction_frame

_state_update_queue = Queue()

main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

create_stt_frame(main_frame)
create_interaction_frame(main_frame)

def set_stt_status(
    text=None,
    record_sec=None,
    silence_sec=None,
    volume=None,
    threshold=None,
    silence_limit=None,
    max_duration=None
):
    update_stt_status(text, record_sec, silence_sec, volume, threshold, silence_limit, max_duration)
    
def _ui_update_loop():
    root.after(0, _update_stt_ui)
    
    root.after(100, _ui_update_loop)

def run():
    root.after(0, _ui_update_loop)    
    root.mainloop()

if __name__ == "__main__":
    run()