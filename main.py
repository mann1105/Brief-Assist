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

# Prompt Templates, Uncomment the one you want to. However, last one is my personal favourite.

# 1. Direct Correction
# PROMPT_TEMPLATE = Template(
#     """Text: $text
#     Instructions: 
#     1. Proofread the text for grammatical errors, including spelling, punctuation, and sentence structure.
#     2. Correct any identified errors.
#     3. Rewrite the corrected text below, maintaining the original meaning and intent as closely as possible.
#     4. In Response you need to provide JUST corrected paragraph so that I can replace it directly."""
# )

# 2.  Style and Tone Enhancement
# PROMPT_TEMPLATE = Template(
#     """Text: $text
#     Instructions:
#     1. Review the text for grammar and punctuation errors. 
#     2. Make necessary corrections to ensure the text is clear and concise.
#     3. In addition to grammatical corrections, evaluate the text for style and tone. Make changes to enhance readability, flow, and overall effectiveness of the writing.
#     4. In Response you need to provide JUST corrected paragraph so that I can replace it directly.
#     """
# )

# 3. Your Personal Grammarly

# Type of document: [Email, Research paper, Social media post, Blog article, Essay, Report]
# Audience:         [Friends, Colleagues, Potential employer, General public, Specific group, Learners]
# Desired tone:     [Formal, Informal, Friendly, Professional, Persuasive, Enthusiastic, ]
# Domain:           [Academic, Business, Technical, Creative, Legal, Medical]

# MODIFY based on the work you are performing
PROMPT_TEMPLATE = Template(
    """Text: $text
    
    Type of document: Email
    Intended audience: Colleagues
    Desired tone: Formal and Objective
    Domain or field: Business
    
    Instructions:
    1. Proofread the text for any grammatical errors (spelling, punctuation, grammar).
    2. Consider the document details and tailor corrections to align with the intended type, audience, tone and domain.
    3. Ensure the corrected text is clear, concise, and effective in achieving its purpose.
    4. In Response you need to provide JUST corrected paragraph so that I can replace it directly.
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
