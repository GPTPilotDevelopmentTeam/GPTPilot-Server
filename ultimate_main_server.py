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
    gen = model.send_message(text, plane_instance)
    
    for g in gen:
        print(f'processing: {g}')
        action.analyzing_message(g, plane_instance)
        tts.text_to_speech(g)


stt.set_transcription_callback(callback)
stt.start()
stt.register_interrupt_callback(model.interrupt)
stt.register_interrupt_callback(tts.interrupt)
tts.start()

ui.run()
    