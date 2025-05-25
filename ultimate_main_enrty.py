from multiprocessing import Process
import tkinter as tk
import subprocess
import sys
import os
import threading
from tkinter import ttk

PROGRESS_SECONDS = 5  # Change this value to set the progress bar duration (in seconds)
PROGRESS_STEPS = 10   # Number of steps for the progress bar
PROGRESS_DELAY = int((PROGRESS_SECONDS / PROGRESS_STEPS) * 1000)  # milliseconds per step

server_process = None
progress_bar = None

def start_server_with_bar():
    start_button.config(state="disabled")
    end_button.config(state="disabled")
    progress_bar["value"] = 0
    threading.Thread(target=increment_bar, args=(0,), daemon=True).start()  # Use a thread to avoid blocking the UI
    run_server()  # Start the server process first

def increment_bar(step):
    if step <= PROGRESS_STEPS:
        progress_bar["value"] = (step / PROGRESS_STEPS) * 100
        root.after(PROGRESS_DELAY, increment_bar, step + 1)
    else:
        start_button.config(state="normal")
        end_button.config(state="normal")

def run_server():
    global server_process
    if server_process is None or server_process.poll() is not None:
        python_exe = sys.executable
        script_path = os.path.join(os.path.dirname(__file__), "ultimate_main_server.py")
        server_process = subprocess.Popen([python_exe, script_path])

def end_server():
    global server_process
    if server_process is not None and server_process.poll() is None:
        server_process.terminate()
        server_process = None

root = tk.Tk()
root.title("GPT Pilot launcher")
root.geometry("400x500")  # Set window size

button_font = ("Arial", 20)

start_button = tk.Button(root, text="Start Server", command=start_server_with_bar, font=button_font, width=15, height=3)
start_button.pack(padx=40, pady=20)

end_button = tk.Button(root, text="End Server", command=end_server, font=button_font, width=15, height=3)
end_button.pack(padx=40, pady=20)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(padx=40, pady=10)
# Initially hidden; will be packed when needed

root.mainloop()

