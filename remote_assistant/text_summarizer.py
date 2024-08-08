import ctypes
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

# Prompt Templates, Uncomment the one you want to. However, 3rd one is my personal favourite.

# 1. Concise Summary
# template = """Text: {text}
    
#     Instructions:
#     1. Summarize the text above in a concise and informative manner. Focus on the main points, key findings, and essential details.
#     2. In Response you need to provide JUST corrected paragraph so that I can replace it directly.
#     """

# 2.  Key Points Extraction(Best for summarizing news or long emails)
# template = """Text: {text}
    
#     Instructions:
#     1. Extract the key points and main arguments from the text above. Present them in a clear and structured list, highlighting the most important information.
#     2. In Response you need to provide JUST corrected paragraph so that I can replace it directly.
#     """

# 3. Abstract Generation (Academic/Research)

template = """Text: {text}
    
    Instructions:
    1. Generate a concise abstract of the text above. Include the main research question, methodology, results, and conclusions. Follow standard academic conventions for abstract formatting.
    2. In Response you need to provide JUST corrected paragraph so that I can replace it directly.
    """
prompt_template = ChatPromptTemplate.from_template(template)
chain = prompt_template | model

def fix_text(text):
    response = chain.invoke({"text": text})
    return response.content

def fix_selection():
    # 1. copy to clipboard
    with controller.pressed(Key.ctrl):
        controller.tap('c')

    # 2. get text from clipboard
    time.sleep(0.1)
    text = pyperclip.paste()

    # 3. process
    fixed_text = fix_text(text)

    # 4. Shows response in a popup
    show_notification("Summarized Text", fixed_text)

def show_notification(title, message, timeout=10):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0)

def fix_current_line():
    controller.press(Key.ctrl)
    controller.press(Key.shift)
    controller.press(Key.left)

    controller.release(Key.ctrl)
    controller.release(Key.shift)
    controller.release(Key.left)

    fix_selection()

def on_f9():
    fix_current_line()

def on_f10():
    fix_selection()

with keyboard.GlobalHotKeys({
        '<120>': on_f9,
        '<121>': on_f10}) as h:
    h.join()
