from openai import OpenAI
import os

class MemoryManager:
    """
    Manages the memory of the model.
    - Short-term memory: immediate conversation
    - Long-term memory: important conversations (flight events prioritized)
    - Aircraft state: current technical state information
    """
    def __init__(self, summary_threshold=10, long_term_memory_size=10):
        self._prompt = []
        self._short_term_memory = []
        self._long_term_memory = []
        self._long_term_memory_size = long_term_memory_size
        self._aircraft_state = ""
        self._summary_model = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        self._summary_threshold = summary_threshold
        
        with open('src/engine/memorization/long_term_memory_prompt.txt', 'r', encoding='utf-8') as f:
            self._long_term_prompt = f.read()
            f.close()
            
        with open('src/engine/memorization/aircraft_state_memory_prompt.txt', 'r', encoding='utf-8') as f:
            self._aircraft_state_prompt = f.read()
            f.close()
        
    def add_prompt(self, prompt: str):
        """Add a prompt to the memory manager."""
        self._prompt.append({'role': 'system', 'content': prompt})
       
    def add_message(self, role: str, content: str):
        """Add a message to the short-term memory."""
        self._short_term_memory.append({"role": role, "content": content})

        if len(self._short_term_memory) >= self._summary_threshold:
            self.process_short_term()

    def process_short_term(self):
        """Process short-term memory into long-term memory and update aircraft state separately."""
        if not self._short_term_memory:
            return

        messages = [{"role": m['role'], "content": m['content']} for m in self._short_term_memory]

        response = self._summary_model.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self._long_term_prompt},
                *messages,
                {"role": "user", "content": "Please summarize the conversation according to the above rules."}
            ],
            temperature=0.2,
        )

        summary_content = response.choices[0].message.content.strip()
        self._long_term_memory.append({"role": "assistant", "content": summary_content})
        if self._long_term_memory and len(self._long_term_memory) > self._long_term_memory_size:
            self._long_term_memory.pop(0)

        state_response = self._summary_model.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self._aircraft_state_prompt},
                *messages,
                *self._long_term_memory,
                {'role': 'system', 'content': f"Current aircraft state: {self._aircraft_state}"},
                {"role": "user", "content": "Please update the aircraft state based on the conversation."}
            ],
            temperature=0.1,
        )

        self._aircraft_state = state_response.choices[0].message.content.strip()

        self._short_term_memory = []

    def get_memory(self):
        """Get the memory for the model."""
        return self._prompt + self._long_term_memory + self._short_term_memory

    def get_aircraft_state(self):
        """Get the current aircraft state description."""
        return self._aircraft_state

    def __str__(self):
        """String representation for debugging."""
        return (
            f"MemoryManager(\n"
            f"\tshort_term_memory={self._short_term_memory},\n"
            f"\tlong_term_memory={self._long_term_memory},\n"
            f"\taircraft_state='{self._aircraft_state}'\n"
            f")"
        )
