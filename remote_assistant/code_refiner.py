from pynput import keyboard
from pynput.keyboard import Key, Controller

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import tempfile
from dotenv import load_dotenv
from string import Template

import os
import pyperclip
import time
import httpx

load_dotenv()
controller = Controller()
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# 1. Direct Correction
template = """Code: {text}

    Instructions:
    1. Improve readability.
    2. Refactor for the specified style guide.
    3. Add comments where changes are made.
    4. Use descriptive variable names.
    5. ONLY return the corrected code.
    """

prompt_template = ChatPromptTemplate.from_template(template)
chain = prompt_template | model

def fix_text(text):
    response = chain.invoke({"text": text})
    return response.content

def fix_selection():
    # 1. copy to clipboard
    with controller.pressed(Key.cmd):
        controller.tap('c')

    # 2. get text from clipborad
    time.sleep(0.1)
    text = pyperclip.paste()

    # 3. process
    fixed_text = fix_text(text)

    # 4. Copies back to clipboard
    pyperclip.copy(fixed_text)
    time.sleep(0.1)

    # 5. Inserts text(cmd v)
    with controller.pressed(Key.cmd):
        controller.tap('v')

def fix_current_line():
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
