from openai import OpenAI
from threading import Thread
from queue import Queue
import json
import sys
import os

sys.path.insert(1, os.getcwd())
from src.utils import LogSystem
from src.engine.memorization import MemoryManager

class InteractionModel:
    """
    Legacy version of the interaction model.
    
    It is slower than the streaming version, but more stable and easier to use.
    If not persuing for faster response, you can use this model.
    
    This class is responsible for the interaction between the user and the pilot.
    By using SendMessage function, the user can send a message to the model and get a response as well as a command.
    """
    def __init__(self):
        self._interactor = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        self._model_name = 'gpt-4o-mini'
        self._temperature = 0.7
        self._max_tokens = 1000
        
        with open('src/engine/interactor_prompt.txt', 'r', encoding='utf-8') as f:
            self._prompt = f.read()
            f.close()
        
        self._memory = MemoryManager()
        self._memory.add_prompt(self._prompt)
        
        self.log = LogSystem("interaction_model")
        self.log("Interaction model initialized.")
        
    def _parse_response(self, response: str):
        lines = response.strip().splitlines()

        talk_response = lines[0]
        json_response = ''.join(lines[1:]).strip()

        commands = None

        if json_response:
            try:
                commands = json.loads(json_response)

                if isinstance(commands, list) and len(commands) == 1 and commands[0].get('action') == 'none':
                    commands = None

            except json.JSONDecodeError:
                commands = None

        return talk_response, commands

    def send_message(self, message: str):
        """This function will send a message to the model and get a response.

        Args:
            message (str): The input message from the user.

        Returns:
            response (str, list): The response from the model, the string is the response and the list is the commands.
        """
        self.log(f"Received message from user: {message}", True)
        completion = self._interactor.chat.completions.create(
            model=self._model_name,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            messages=self._memory.get_memory() + [{"role": "user", "content": message}]
        )
        
        self.log("Processing response from model...")
        talk_response, commands = self._parse_response(completion.choices[0].message.content)
        self.log(f"Response from model: {talk_response}", True)
        self.log(f"Commands from model: {commands}", True)
        
        self._memory.add_message("user", message)
        self._memory.add_message("assistant", talk_response)
        
        self.log("Response processed.\nUpdated memory: \n" + str(self._memory))
        return talk_response, commands
    
    
class StreamInteractionModel:
    def __init__(self):
        self._interactor = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        self._model_name = 'gpt-4o-mini'
        self._temperature = 0.7
        self._max_tokens = 1000
        
        with open('src/engine/interactor_prompt.txt', 'r', encoding='utf-8') as f:
            self._prompt = f.read()
            f.close()
        with open('src/engine/stream_prompt.txt', 'r', encoding='utf-8') as f:
            self._prompt += f.read()
            f.close()
        
        self._memory = MemoryManager()
        self._memory.add_prompt(self._prompt)
        self._is_interrupted = False
        
        self.log = LogSystem("streaming_interaction_model")
        self.log("Interaction model initialized.")
        
    def _parse_message(self, stream):
        text_buf = ""
        self._is_interrupted = False
        for event in stream:
            content = event.choices[0].delta.content
            
            if content is None:
                continue
            if self._is_interrupted:
                return
            
            text_buf += content

            if '[END]' in text_buf:
                text_buf = text_buf.replace('[END]', '')
                self._memory.add_message('assistant', text_buf)
                yield text_buf
                text_buf = ""
        
        if len(text_buf) > 0:
            text_buf = text_buf.replace('[END]', '')
            self._memory.add_message('assistant', text_buf)
            yield text_buf

    def send_message(self, message: str, plane=None):
        """This function will send a message to the model and return a generator that yields the response."""
        
        plane_state = {'role': 'system', 'content': 'The current state of the plane is ' + str(plane)} if plane else {'role': 'system', 'content': 'The current state of the plane is unknown.'}
        self.log(f"Received message from user: {message}", True)
        self._memory.add_message("user", message)
        stream = self._interactor.chat.completions.create(
            model=self._model_name,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            messages=[plane_state] + self._memory.get_memory(), 
            stream=True
        )
        self._is_interrupted = True
        
        self.log("Returning generator")
        return self._parse_message(stream)
    
class ActionDeterminationModel:
    def __init__(self, output_callback=None):
        self._interactor = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        self._model_name = 'gpt-4o-mini'
        self._temperature = 0.7
        self._max_tokens = 1000
        
        with open('src/engine/action_prompt.txt', 'r', encoding='utf-8') as f:
            self._prompt = f.read()
            f.close()
            
        if output_callback is None:
            self._output_callback = lambda x: print(x)
        else:
            self._output_callback = output_callback
        
        self.message_queue = Queue()
        Thread(target=self._worker, args=(self.message_queue,), daemon=True).start()
        self.log = LogSystem("action_determination_model")
        self.log("Action determination model initialized.")
        
    def _worker(self, message_queue: Queue):
        while True:
            message = self.message_queue.get()
            if message is None:
                break
            completion = self._interactor.chat.completions.create(
                model=self._model_name,
                temperature=self._temperature,
                max_tokens=self._max_tokens,
                messages=[{'role': 'system', 'content': self._prompt}, {"role": "user", "content": message}]
            )
            
            self.log("Processing response from model...")
            jsons = completion.choices[0].message.content
            
            self.log(f"Response from model: {jsons}", True)
            self._output_callback(jsons)
            message_queue.task_done()
        
    def analyzing_message(self, message: str, plane=None):
        self.message_queue.put(f'plane state: {plane}\n\npilot\'s instruction:{message}')