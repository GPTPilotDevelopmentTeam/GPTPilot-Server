from threading import Thread, Lock, current_thread
from queue import Queue
from pygame import mixer
import os
import sys
import time

sys.path.insert(1, os.getcwd())
from src.app.tts_engine import openai_tts
from src.utils import LogSystem

log = LogSystem("tts")

_processing_func = None
_proc_funcs = {'whisper': openai_tts.text_to_speech}

_thread_pool = Queue()
_chart_lock = Lock()
_queue_lock = Lock()
_audio_chart = {}
_is_interrupted = False

def _play_audio():
    global _thread_pool, _audio_chart, _chart_lock, _queue_lock, _is_interrupted
    while True:
        if not _thread_pool.empty():
            thread = _thread_pool.get()
            id = thread.ident
            thread.join()
            
            with _chart_lock:
                log(f'Thread {id} finished processing')
                log(f'Start playing audio: {_audio_chart[id]}')
                
                mixer.music.load(_audio_chart[id])
                mixer.music.play()
                
            while mixer.music.get_busy() and not _is_interrupted:
                time.sleep(0.1)
            
            mixer.music.stop()
                
            while _is_interrupted:
                try:
                    thread = _thread_pool.get_nowait()
                    thread.join()
                    if thread.ident in _audio_chart:
                        os.remove(_audio_chart[thread.ident])
                        _audio_chart.pop(thread.ident)
                    _thread_pool.task_done()
                except:
                    _queue_lock.release()
                    break  # Queue is empty, exit the loop

            _is_interrupted = False
            log('Audio playback finished')
            _audio_chart.pop(id)
        else:
            time.sleep(.5)
            
def interrupt():
    global _is_interrupted, _queue_lock
    
    log('Interrupting audio playback...')
    if mixer.music.get_busy():
        _is_interrupted = True
        _queue_lock.acquire()
        

def start(proc_func='whisper'):
    global _processing_func, _proc_funcs
    log('Initializing tts module...', True)

    _processing_func = _proc_funcs.get(proc_func, _proc_funcs['whisper'])

    log('Starting audio player...')
    Thread(target=_play_audio, daemon=True).start()
    mixer.init()

    log('TTS module initialized successfully.', True)

def _process_text_segment(segment: str):
    global _chart_lock, _audio_chart

    log(f'Thread {current_thread().ident} start processing')
    audio_path = _processing_func(segment)
    log(f'Thread {current_thread().ident} finished processing, get audio path: {audio_path}')
    with _chart_lock:
        _audio_chart[current_thread().ident] = audio_path

def text_to_speech(texts: str):
    global _thread_pool
    
    log(f"Processing text: {texts}")
    thread = Thread(target=_process_text_segment, args=(texts,))
    thread.start()
    log(f"Thread {thread.ident} process text: {texts}")

    with _queue_lock:
        _thread_pool.put(thread)
        