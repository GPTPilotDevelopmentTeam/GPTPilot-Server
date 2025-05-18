import sys
import os

sys.path.insert(1, os.getcwd())
from src.engine.interaction_model import ActionDeterminationModel

model = ActionDeterminationModel()

model.analyzing_message("Hello, how are you?")
model.analyzing_message("What is the weather like today?")
model.analyzing_message("Gear down.")
model.analyzing_message("Flap 10.")
model.analyzing_message("Set altitude to 1000 feet, flap 30.")