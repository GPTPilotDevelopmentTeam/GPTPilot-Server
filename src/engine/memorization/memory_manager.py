from openai import OpenAI
import os


class MemoryManager:
    """
    Manages the memory of the model.
    """
    def __init__(self, summary_threshold=10):
        self._prompt = []
        self._short_term_memory = []
        self._long_term_memory = []
        self._summary_model = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY")
        )
        self._summary_threshold = summary_threshold
        
    def add_prompt(self, prompt: str):
        """Add an prompt to the memory manager."""
        self._prompt.append({'role': 'system', 'content': prompt})
       
    def add_message(self, role: str, content: str):
        """Add a message to the short-term memory."""
        if (len(self._short_term_memory) > self._summary_threshold):
            self.generate_summary()

        self._short_term_memory.append({"role": role, "content": content})

         
    def generate_summary(self):
        """Generate a summary of the short-term memory and store it in long-term memory."""
        if not self._short_term_memory:
            return
        
        message = [{"role": m['role'], "content": m['content']} for m in self._short_term_memory]
        system_prompt = (
            "You are an aircraft copilot memory recorder.\n\n"
            "Your task is to summarize the following conversation, but only include information that is directly relevant to the operation, state, or important decisions regarding the aircraft.\n\n"
            "Strictly follow these rules:\n"
            "- Ignore any small talk, personal conversations, jokes, or irrelevant discussions (e.g., about food, weather, feelings, etc.).\n"
            "- Only extract information related to: flight instructions, aircraft status, operational actions, emergency handling, or critical updates.\n"
            "- If a message does not affect the aircraft or the flight operation, you MUST omit it.\n"
            "- Be concise, use direct factual statements.\n"
            "- Do not invent or speculate missing details.\n\n"
            "Output only the important flight-related facts in simple English."
        )
   
        response = self._summary_model.chat.completions.create(
            model='gpt-4o',
            messages=[
                {'role': 'system', 'content': system_prompt},
                *message,
                {'role': 'user', 'content': "Please summarize the above messages."}
            ],
            temperature=0.2
        )
        
        summary_content = response.choices[0].message.content.strip()
        
        self._long_term_memory.append({"role": "assistant", "content": summary_content})
        self._short_term_memory = []

    def get_memory(self):
        """Get the memory for the model."""
        return self._prompt + self._long_term_memory + self._short_term_memory