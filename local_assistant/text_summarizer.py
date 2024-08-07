import pyperclip
import tempfile
import os
import time
import httpx

from string import Template
from pynput import keyboard
from pynput.keyboard import Key, Controller

controller = Controller()

OLLAMA_ENDPOINT =  "http://localhost:11434/api/generate" 
OLLAMA_CONFIG = {"model": "phi3:3.8b",
                 "stream" : False,
                 "keep_alive": "5m"
}  

# Prompt Templates, Uncomment the one you want to.

# 1. Concise Summary
# PROMPT_TEMPLATE = Template(
#     """Text: $text
    
#     Instructions:
#     1. Summarize the text above in a concise and informative manner. Focus on the main points, key findings, and essential details.
#     2. In Response you need to provide JUST corrected paragraph so that I can replace it directly."""
# )

# 2. Key Points Extraction(Best for summarizing news or long emails)
# PROMPT_TEMPLATE = Template(
#     """Text: $text
    
#     Instructions:
#     1. Extract the key points and main arguments from the text above. Present them in a clear and structured list, highlighting the most important information.
#     2. In Response you need to provide JUST corrected paragraph so that I can replace it directly."""
# )

# 3. Abstract Generation (Academic/Research)
PROMPT_TEMPLATE = Template(
    """Text: $text
    
    Instructions:
    1. Generate a concise abstract of the text above. Include the main research question, methodology, results, and conclusions. Follow standard academic conventions for abstract formatting.
    2. In Response you need to provide JUST corrected paragraph so that I can replace it directly."""
)


def fix_text(text):
    prompt = PROMPT_TEMPLATE.substitute(text=text)
    
    response = httpx.post(
        OLLAMA_ENDPOINT,
        json={"prompt": prompt, **OLLAMA_CONFIG},
        headers={"Content-Type": "application/json"},
        timeout=30,
    )

    if response.status_code != 200:
        return None
    
    return response.json()['response'].strip()

def fix_current_line():
    # cmd + shift + left
    controller.press(Key.cmd)
    controller.press(Key.shift)
    controller.press(Key.left)

    controller.release(Key.cmd)
    controller.release(Key.shift)
    controller.release(Key.left)

    fix_selection()

def fix_selection():
    # 1. Copy to clipboard(cmd c)
    with controller.pressed(Key.cmd):
        controller.tap('c')

    # 2. Get's text
    time.sleep(0.1)
    text = pyperclip.paste()
    # print(text)

    # 3. Fixies text
    fixed_text = fix_text(text)

    # 4. Shows response on screen
    show_notification("Summarized Text", fixed_text)

def show_notification(title, message, timeout=10):
    with tempfile.NamedTemporaryFile(mode='w+t', suffix='.txt', delete=False) as temp_file:
        temp_file.write(message)
        os.system(f'open -a TextEdit {temp_file.name}')  

def on_f9():
    fix_current_line()

def on_f10():
    fix_selection()

with keyboard.GlobalHotKeys({
        '<101>': on_f9,
        '<109>': on_f10}) as h:
    h.join()
