from threading import Thread, Lock, current_thread
from queue import Queue
import playsound
import os
import sys
import time

sys.path.insert(1, os.getcwd())
from src.app.tts_engine import openai_tts

_processing_func = None
_proc_funcs = {'whisper': openai_tts.text_to_speech}

_thread_pool = Queue()
_chart_lock = Lock()
_audio_chart = {}
_audio_player = None

def _play_audio():
    global _thread_pool, _audio_chart
    while True:
        if not _thread_pool.empty():
            thread = _thread_pool.get()
            id = thread.ident
            thread.join()
            
            playsound.playsound(_audio_chart[id])
            os.remove(_audio_chart[id])
            _audio_chart.pop(id)
        else:
            time.sleep(.5)

def start(proc_func='whisper'):
    global _processing_func, _proc_funcs, _audio_player
    _processing_func = _proc_funcs.get(proc_func, _proc_funcs['whisper'])
    _audio_player = Thread(target=_play_audio, daemon=True)
    _audio_player.start()

def _process_text_segment(segment: str):
    global _chart_lock, _audio_chart
    audio_path = _processing_func(segment.strip())
    with _chart_lock:
        _audio_chart[current_thread().ident] = audio_path

def text_to_speech(texts: str):
    global _thread_pool
    
    thread = Thread(target=_process_text_segment, args=(texts,))
    thread.start()
    _thread_pool.put(thread)
