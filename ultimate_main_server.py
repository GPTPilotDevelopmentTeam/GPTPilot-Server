from src import Server
from src.app import stt, tts
from src.engine import StreamInteractionModel
from src.udp import Plane
from src import ui
import time

model = StreamInteractionModel()
plane_instance = Plane()

def callback(text):
    global model
    print(f'User says: {text}')
    gen = model.send_message(text, plane_instance)
    tts.interrupt()
    
    for g in gen:
        print(f'processing: {g}')
        tts.text_to_speech(g)


if __name__ == '__main__':
    stt.set_transcription_callback(callback)
    stt.start()
    tts.start()
    server_instance = Server()
    server_instance.run_tcp_server()
    ui.run()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Main program interrupted. Exiting...")