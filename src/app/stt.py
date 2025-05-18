from queue import Queue
from threading import Thread
import sounddevice as sd
import numpy as np
import whisper
import sys
import os
import io
import contextlib
import time

sys.path.insert(1, os.getcwd())
from src.utils import LogSystem

log = LogSystem("stt")
"""Log system for STT."""

log('Initializing stt module...', True)

THRESHOLD = 0.4
"""When the volume is lower than this value, it is considered to be silent."""

SLIENCE_DURATION = 1.0
"""How long to pause before considering it finished (seconds)."""

SAMPLE_RATE = 16000

BLOCK_SIZE = 1024
"""Number of samples read each time."""

MAX_RECORDING_DURATION = 5.0
"""Maximum recording duration (seconds)."""

_is_running = False
"""Flag to indicate if the audio processing is started."""

_transcription_queue = Queue()
"""Queue to store audio data for processing."""

_transcription_callback = lambda text : print("Transcribed text: ", text)
"""The callback function to receive the transcribed text."""

_audio_transcribing_thread = None
""""Thread for audio transcribing."""

_monitoring_thread = None
""""Thread for monitoring microphone and detecting speech."""

_model_name = 'turbo'

try:
    _model = whisper.load_model(_model_name).to("cuda")
    log('[STT]: Find gpu.', True)
except:
    _model = whisper.load_model(_model_name).to("cpu")
    log('[STT]: GPU not found, using cpu.', True)
"""The Whisper model."""

def _monitor_microphone():
    """Background thread that monitors the microphone, detects speech, and pushes audio to the queue."""
    global _is_running, _transcription_queue

    log("Listening to microphone (continuous mode)...")

    stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='float32', blocksize=BLOCK_SIZE)

    with stream:
        # 預熱避免啟動延遲
        for _ in range(3):
            stream.read(BLOCK_SIZE)

        recording = []
        silent_chunks = 0
        has_speak = False

        while _is_running:
            audio_block, _ = stream.read(BLOCK_SIZE)
            audio_block = np.squeeze(audio_block)

            recording.append(audio_block)

            volume_norm = np.linalg.norm(audio_block)  # Measure volume intensity

            if volume_norm < THRESHOLD:
                silent_chunks += 1
            else:
                silent_chunks = 0  # Reset if there is sound
                has_speak = True

            if silent_chunks * (BLOCK_SIZE / SAMPLE_RATE) > SLIENCE_DURATION and has_speak:
                audio = np.concatenate(recording)
                log(f"Detected speech with {len(audio) / SAMPLE_RATE:.2f} seconds.")
                push_transcribe_audio(audio)
                recording = []
                silent_chunks = 0
                has_speak = False

            if len(recording) * (BLOCK_SIZE / SAMPLE_RATE) > MAX_RECORDING_DURATION:
                if has_speak:
                    audio = np.concatenate(recording)
                    log("Max duration reached, auto cutting...")
                    push_transcribe_audio(audio)
                else:
                    log("Record nothing, skipping.")
                recording = []
                silent_chunks = 0
                has_speak = False


def _transcribing_audio():
    """Thread function to transcribe audio."""
    global _model, _transcription_queue, _is_running, _transcription_callback
    while _is_running:
        if _transcription_queue.empty():
            time.sleep(0.1)
            continue

        audio = _transcription_queue.get()
        log(f"Transcribing audio with {len(audio) / SAMPLE_RATE:.2f} seconds...")

        # Redirect verbose output to a string
        verbose_output = io.StringIO()
        with contextlib.redirect_stdout(verbose_output):
            result = _model.transcribe(audio, verbose=True)

        text = result["text"]
        verbose_log = verbose_output.getvalue()  # Get the verbose output as a string
        verbose_output.close()

        _transcription_callback(text)
        log(f"Verbose output:\n{verbose_log}")


def set_transcription_callback(callback):
    """Set the callback function to receive the transcribed text.

        Parameters
        ----------
        callback : function
            The callback function to receive the transcribed text.
    """
    global _transcription_callback
    _transcription_callback = callback


def push_transcribe_audio(audio):
    """Push the audio data to the queue for transcription.

        Parameters
        ----------
        audio : numpy.ndarray
            The audio data to be transcribed.
    """
    global _transcription_queue
    _transcription_queue.put_nowait(audio)


def start():
    """Start the audio processing functionality."""
    log("Starting audio transcribe system...", True)

    global _is_running, _audio_transcribing_thread, _monitoring_thread
    _is_running = True

    _audio_transcribing_thread = Thread(target=_transcribing_audio, daemon=True)
    _audio_transcribing_thread.start()

    _monitoring_thread = Thread(target=_monitor_microphone, daemon=True)
    _monitoring_thread.start()

    log("Done! You may start talking.", True)
    log("Audio transcribe system started with the following parameters:")
    log(f"THRESHOLD: {THRESHOLD}")
    log(f"SLIENCE_DURATION: {SLIENCE_DURATION}")
    log(f"SAMPLE_RATE: {SAMPLE_RATE}")
    log(f"BLOCK_SIZE: {BLOCK_SIZE}")
    log(f"MAX_RECORDING_DURATION: {MAX_RECORDING_DURATION}")


def stop():
    """Stop the audio processing functionality."""
    log("Stopping audio transcribe system...", True)

    global _is_running, _audio_transcribing_thread, _monitoring_thread
    _is_running = False

    _audio_transcribing_thread.join()
    _audio_transcribing_thread = None

    _monitoring_thread.join()
    _monitoring_thread = None

    log("Audio transcribe system stopped.", True)

