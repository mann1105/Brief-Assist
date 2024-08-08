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

# Prompt Templates, Uncomment the one you want to. However, 3rd one is my personal favourite.

# 1. Direct Correction
template = """Text: {text}
    Instructions: 
    1. Proofread the text for grammatical errors, including spelling, punctuation, and sentence structure.
    2. Correct any identified errors.
    3. Rewrite the corrected text below, maintaining the original meaning and intent as closely as possible.
    4. In Response you need to provide JUST corrected paragraph so that I can replace it directly.
    """

# 2.  Style and Tone Enhancement
# template = """Text: {text}
#     Instructions:
#     1. Review the text for grammar and punctuation errors. 
#     2. Make necessary corrections to ensure the text is clear and concise.
#     3. In addition to grammatical corrections, evaluate the text for style and tone. Make changes to enhance readability, flow, and overall effectiveness of the writing.
#     4. In Response you need to provide JUST corrected paragraph so that I can replace it directly.
#     """

# 3. Your Personal Grammarly

# Type of document: [Email, Research paper, Social media post, Blog article, Essay, Report]
# Audience:         [Friends, Colleagues, Potential employer, General public, Specific group, Learners]
# Desired tone:     [Formal, Informal, Friendly, Professional, Persuasive, Enthusiastic, ]
# Domain:           [Academic, Business, Technical, Creative, Legal, Medical]

# MODIFY based on the work you are performing
# template = """Text: {text}
    
#     Type of document: Email
#     Intended audience: Colleagues
#     Desired tone: Formal and Objective
#     Domain or field: Business
    
#     Instructions:
#     1. Proofread the text for any grammatical errors (spelling, punctuation, grammar).
#     2. Consider the document details and tailor corrections to align with the intended type, audience, tone and domain.
#     3. Ensure the corrected text is clear, concise, and effective in achieving its purpose.
#     4. Follow the format required in specific documents like in email start with Dear ... as per the context of the paragraph and end with appropriate ending like Thank you/ yours sciencerly.
#     5. In Response you need to provide JUST corrected paragraph so that I can replace it directly.
#     """
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
