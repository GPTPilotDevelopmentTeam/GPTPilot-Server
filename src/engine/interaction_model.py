import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from memorization import MemoryManager
from openai import OpenAI
import json

class InteractionModel:
    """
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
        print(f"Received message: {message}")
        completion = self._interactor.chat.completions.create(
            model=self._model_name,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            messages=self._memory.get_memory() + [{"role": "user", "content": message}]
        )
        
        talk_response, commands = self._parse_response(completion.choices[0].message.content)
        
        self._memory.add_message("user", message)
        self._memory.add_message("assistant", talk_response)
        return talk_response, commands