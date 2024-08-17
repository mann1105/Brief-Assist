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
    print(f"Original text: {text}")  # Debugging print
    
    try:
        # Call the model to get the response
        response = chain.invoke({"text": text, "chat_history": chat_history})
        
        # Ensure the response is valid and not empty
        if not response or not response.content:
            print("Error: Received an empty response from the model.")
            return "No response received", chat_history
        
        print(f"Model response: {response.content}")  # Debugging print
        return response.content, chat_history + f"User: {text}\nAssistant: {response.content}\n"
    
    except Exception as e:
        # Print the error if something goes wrong with the model invocation
        print(f"Error during model invocation: {e}")
        return "Error invoking the model", chat_history

def fix_selection():
    global chat_history
    # 1. Copy text (Ctrl+C in Windows)
    with controller.pressed(Key.ctrl):
        controller.tap('c')

    # 2. Copy to Clipboard
    time.sleep(0.2)  # Increased the sleep time to ensure clipboard operation works
    text = pyperclip.paste()
    print(f"Text copied from clipboard: {text}")  # Debugging print
    
    # If no text is copied, return early
    if not text.strip():
        print("No text was selected/copied.")
        return
    
    # 3. Generate the Response
    fixed_text, chat_history = fix_text(text, chat_history)
    final_text = f"{text}\n\n{fixed_text}"

    # 4. Copy back to clipboard
    pyperclip.copy(final_text)
    time.sleep(0.2)  # Added a slight delay before pasting
    print("Text successfully copied back to clipboard")

    # 5. Paste back (Ctrl+V in Windows)
    with controller.pressed(Key.ctrl):
        controller.tap('v')

    # Add a new line for the next user question
    controller.press(Key.enter)
    controller.release(Key.enter)

def fix_current_line():
    global chat_history
    # Select current line (Ctrl+Shift+Left in Windows)
    controller.press(Key.ctrl)
    controller.press(Key.shift)
    controller.press(Key.left)
    controller.release(Key.ctrl)
    controller.release(Key.shift)
    controller.release(Key.left)
    fix_selection()

def on_f9():
    fix_current_line()

# Set up a global hotkey (F9) in Windows
with keyboard.GlobalHotKeys({
        '<120>': on_f9, }) as h:
    h.join()
