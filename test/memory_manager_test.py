import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

from src.engine.memorization import MemoryManager

mm = MemoryManager(summary_threshold=3)
mm.add_prompt("You are a copilot in an airplane cockpit. You are assisting the pilot in handling emergencies. Please provide clear instructions and suggestions to the pilot. " \
               "You are not allowed to ask questions. You are not allowed to say 'I don't know'. " \
               "You are not allowed to say 'I am not sure'. You are not allowed to say 'I cannot help you'. " \
               "You are not allowed to say 'I am not a pilot'. You are not allowed to say 'I am not a copilot'." \
               "Say a sentence is enough, and do not say too much.")

test_messages = [
    "爬行至3000英尺後保持平穩飛行",
    "今天天氣怎麼樣？",
    "請幫我檢查一下油量",
    "你今天晚餐吃甚麼？",
    "等等下飛機後你要吃甚麼？",
    "收起起落架"
]

fake_responses = [
    "好的，爬行至3000英尺後保持平穩飛行。",
    "今天陽光明媚，於是我們決定做這個企劃，早餐吃到飽",
    "油量正常，還有1000公里的航程",
    "今天晚餐吃牛排",
    "我想吃義大利麵",
    "起落架已收起，保持穩定飛行"
]

for idx, message in enumerate(test_messages):
    print(f"Iteration {idx + 1}\nwith message: {message}")
    mm.add_message("user", message)
    mm.add_message("assistant", fake_responses[idx])
    print("Current memory state:")
    print('short term memory:', mm._short_term_memory)
    print('long term memory:', mm._long_term_memory)
    print('\n')
    