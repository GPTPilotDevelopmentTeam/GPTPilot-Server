import tkinter as tk
from tkinter import ttk

interaction_output = tk.StringVar(value="尚未開始")

def create_interaction_frame(parent):
    interaction_frame = ttk.LabelFrame(parent, text="🧠 Interaction Model")
    interaction_frame.pack(fill="x", padx=5, pady=5)

    ttk.Label(interaction_frame, text="正在輸出中:").pack(anchor="w", padx=5, pady=2)
    interaction_label = ttk.Label(interaction_frame, textvariable=interaction_output, background="white", anchor="w")
    interaction_label.pack(fill="x", padx=5, pady=(0, 5))
