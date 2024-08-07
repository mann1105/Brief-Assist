import pyperclip
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
# 1. General Code Refinement
PROMPT_TEMPLATE = Template(
    """Code: $text

    Instructions:
    1. Improve readability.
    2. Refactor for the specified style guide.
    3. Add comments.
    4. Use descriptive variable names.
    5. ONLY return the corrected code.
    """
)

def fix_text(text):
    prompt = PROMPT_TEMPLATE.substitute(text=text)
    
    response = httpx.post(
        OLLAMA_ENDPOINT,
        json={"prompt": prompt, **OLLAMA_CONFIG},
        headers={"Content-Type": "application/json"},
        timeout=45,
    )
    if response.status_code != 200:
        return None
    
    return response.json()['response'].strip()

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

    # 4. Copies back to clipboard
    pyperclip.copy(fixed_text)
    time.sleep(0.1)

    # 5. Inserts text(cmd v)
    with controller.pressed(Key.cmd):
        controller.tap('v')

def fix_current_line():
    # cmd + shift + left
    controller.press(Key.cmd)
    controller.press(Key.shift)
    controller.press(Key.left)

    controller.release(Key.cmd)
    controller.release(Key.shift)
    controller.release(Key.left)

    fix_selection()

def on_f9():
    fix_current_line()

def on_f10():
    fix_selection()

with keyboard.GlobalHotKeys({
        '<101>': on_f9,
        '<109>': on_f10}) as h:
    h.join()
