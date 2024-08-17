from pynput import keyboard
from pynput.keyboard import Key, Controller
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from string import Template
import pyperclip
import time
import httpx

load_dotenv()
controller = Controller()
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# 1. Translation Prompt, Change your 
template = """Text: {text}
    Source Language: English
    Target Language: Gujarati

    Instructions:
    1. Carefully analyze the English text, paying close attention to nuances, idioms, and cultural references.
    2. Translate the text into Gujarati, ensuring that the meaning, tone, and style of the original text are preserved as accurately as possible.
    3. Verify that the translation is grammatically correct and fluent in Gujarati.
    4. If there are any ambiguities or potential misinterpretations in the English text, prioritize clarity and accuracy in the translation, even if it means sacrificing a direct word-for-word translation. 
    5. Provide any additional notes or explanations if needed to clarify cultural references or idioms that might not have direct Gujarati equivalents.
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

    # 2. get text from clipborad
    time.sleep(0.1)
    text = pyperclip.paste()

    # 3. process
    fixed_text = fix_text(text)

    # 4. copy back to clip board
    pyperclip.copy(fixed_text)
    time.sleep(0.1)

    # 5. insert text
    with controller.pressed(Key.ctrl):
        controller.tap('v')


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
