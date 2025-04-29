import threading
import time

import sys
import os
sys.path.insert(1, os.getcwd())
from src.utils.log_system import LogSystem

def stress_test_log_system():
    """Stress test for LogSystem."""
    log = LogSystem("stress_test")
    l = [log, LogSystem("stress_test_1"), LogSystem("stress_test_2"), LogSystem("stress_test_3")]

    def write_logs(thread_id):
        for i in range(1000):
            for log_instance in l:
                log_instance.log(f"Thread-{thread_id}: Log entry {i}")
                time.sleep(0.01)

    # Create multiple threads to write logs simultaneously
    threads = [threading.Thread(target=write_logs, args=(i,)) for i in range(5)]

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Test thread restart after a long duration
    time.sleep(5)
    log("Testing thread restart after long duration.")

    for log_instance in l:
        for i in range(100):
            log_instance.log(f"Log entry {i} after long duration")

    
    # Close the log system
    for log_instance in l:
        log_instance.close()
    
if __name__ == "__main__":
    stress_test_log_system()

