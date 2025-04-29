from datetime import datetime
from queue import Queue
from threading import Thread
import os
import time
import atexit

print("Initalizing log system...")
_log_sys_instances = []
"""Store all log system instances."""

_log_names = set()
"""Memorizing all log names to avoid conflict"""

# Get the absolute path of LOG_PATH relative to the workspace
workspace_dir = os.getcwd()
LOG_PATH = os.path.abspath(os.path.join(workspace_dir, 'logs'))

# Create a directory in LOG_PATH with the current timestamp
timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
_log_dir = os.path.join(LOG_PATH, timestamp)
os.makedirs(_log_dir, exist_ok=True)

print("Log system initialized, log file will located at: ", _log_dir)

class LogSystem:
    """A simple logging system that support multi-threaded logging.
    """
    def __init__(self, name: str):
        if name in _log_names:
            name = name + '_'
        self._name = name
        _log_names.add(name)

        self._log_file = open(os.path.join(_log_dir, f'{name}.log'), 'a', encoding='utf-8')
        if self._log_file.closed:
            raise Exception(f"Log file {name} is closed.")
        
        self._is_write_thread_running = False
        self._write_queue = Queue()
        self._write_queue.put(f"Log system {name} initialized at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self._write_thread = None
        self._restart_write_thread()

        global _log_sys_instances
        _log_sys_instances.append(self)

    def _process_log_queue(self):
        """Process the log queue in a separate thread."""
        none_cnt = 0
        while none_cnt < 50 and self._is_write_thread_running:
            try:
                message = self._write_queue.get_nowait()
                none_cnt = 0
                self._log_file.write(message)
                self._log_file.flush()
            except:
                none_cnt += 1
                time.sleep(0.1)
                continue
        self._is_write_thread_running = False

    def _restart_write_thread(self):
        """Restart the write thread if it has stopped."""
        if not self._is_write_thread_running:
            self._is_write_thread_running = True
            if self._write_thread is not None:
                self._write_thread.join()
            self._write_thread = Thread(target=self._process_log_queue, daemon=True)
            self._write_thread.start()

    def log(self, message: str, pt=False):
        """Log a message to the log file."""
        if pt:
            print(message)
        self._restart_write_thread()
        self._write_queue.put(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        
    def __call__(self, message: str, pt=False):
        """Log a message to the log file."""
        self.log(message, pt=pt)
        
    def close(self, wait: bool = True):
        """Close the log file and stop the write thread.

        Args:
            wait (bool, optional): Determines whether to wait for the write thread to finish. Defaults to True.
        """
        self.log(f"Closing log system {self._name}...")
        if wait and not self._write_queue.empty():
            time.sleep(.1) # just wait
            if not self._is_write_thread_running: # Handling edge case when the thread is not running
                self._restart_write_thread()
        else:
            self._is_write_thread_running = False

        self._write_thread.join()
        self._log_file.close()
        global _log_names, _log_sys_instances
        _log_names.remove(self._name)
        _log_sys_instances.remove(self)
        
def _cleanup_log_systems():
    """Cleanup function to close all log system instances."""
    global _log_sys_instances
    for log_sys in _log_sys_instances[:]:
        log_sys.close(wait=True)

# Register the cleanup function to be called at program exit
atexit.register(_cleanup_log_systems)