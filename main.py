from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyperclip
import time
import httpx
from string import Template

controller = Controller()

OLLAMA_ENDPOINT =  "http://localhost:11434/api/generate" 
 
OLLAMA_CONFIG = {"model": "mistral:7b-instruct-v0.2-q3_K_L",
                 "stream" : False,
                 "keep_alive": "5m"
}  

PROMPT_TEMPLATE = Template(
    """Summarize the following text in one to two sentences:

$text
"""
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
    # 1. copy to clipboard(cmd c)
    with controller.pressed(Key.cmd):
        controller.tap('c')

    # 2. get text
    time.sleep(0.1)
    text = pyperclip.paste()
    # print(text)

    # 3. fix text
    fixed_text = fix_text(text)

    # 4. copy back to clipboard
    pyperclip.copy(fixed_text)
    time.sleep(0.1)

    # 5. insert text(cmd v)
    with controller.pressed(Key.cmd):
        controller.tap('v')


def on_f9():
    fix_current_line()

def on_f10():
    fix_selection()

# from pynput.keyboard import Key
# print(Key.ctrl_l.value, Key.ctrl_r.value)

with keyboard.GlobalHotKeys({
        '<101>': on_f9,
        '<109>': on_f10}) as h:
    h.join()




