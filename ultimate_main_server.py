from src import Server
from src.app import stt, tts
from src.engine import StreamInteractionModel, ActionDeterminationModel
from src.udp import Plane
from src import ui

model = StreamInteractionModel()
plane_instance = Plane()
server_instance = Server()
server_instance.run_tcp_server()

action = ActionDeterminationModel(lambda x: server_instance.send_message(x))

def callback(text):
    global model
    print(f'User says: {text}')
    action.analyzing_message(text)
    gen = model.send_message(text, plane_instance)
    tts.interrupt()
    
    for g in gen:
        print(f'processing: {g}')
        tts.text_to_speech(g)


if __name__ == '__main__':
    stt.set_transcription_callback(callback)
    stt.start()
    tts.start()
    
    ui.run()
    