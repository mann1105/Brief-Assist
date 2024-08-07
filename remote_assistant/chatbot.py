from pynput import keyboard
from pynput.keyboard import Key, Controller
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import pyperclip
import time
import httpx

load_dotenv()
controller = Controller()
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

template = """
            {chat_history}
            User: {text}
            Assistant:
        """ 
prompt_template = ChatPromptTemplate.from_template(template)
chain = prompt_template | model

chat_history = "" 

def fix_text(text, chat_history=""):
    response = chain.invoke({"text": text, "chat_history": chat_history})
    return response.content, chat_history + f"User: {text}\nAssistant: {response.content}\n"

def fix_selection():
    global chat_history
    # 1. Copy text
    with controller.pressed(Key.cmd):
        controller.tap('c')

    # 2. Copy to Clipboard
    time.sleep(0.1)
    text = pyperclip.paste()
    
    # 3. Generate the Response
    fixed_text, chat_history = fix_text(text, chat_history)
    final_text = f"{text}\n\n{fixed_text}"

    # 4. Copy back to clipboard
    pyperclip.copy(final_text)
    time.sleep(0.1)

    # 5. Paste back
    with controller.pressed(Key.cmd):
        controller.tap('v')

    # Add a new line for the next user question
    controller.press(Key.enter)
    controller.release(Key.enter)

def fix_current_line():
    global chat_history
    controller.press(Key.cmd)
    controller.press(Key.shift)
    controller.press(Key.left)
    controller.release(Key.cmd)
    controller.release(Key.shift)
    controller.release(Key.left)
    fix_selection()

def on_f9():
    fix_current_line()

with keyboard.GlobalHotKeys({
        '<101>': on_f9, }) as h:
    h.join()