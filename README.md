****Brief-Assist****


This project provides functionality to summarize or correct grammer of selected text using the mistral:7b-instruct-v0.2-q3_K_L model hosted locally via Ollama. 
The project includes hotkey functionality to streamline text selection and summarization in any application. 
There are many possibities of how you can use these project, some of the examples are summarization, grammar correction, sentence translation, language translation(subject to LLM).

**Prerequisites**
Python 3.7+
Ollama Server: The main.py expects an Ollama server to be running locally on http://localhost:11434.

**Ollama Setup**
1) Installing Ollama
   - Follow the installation instructions from the official Ollama documentation for you PC.
2) Start Ollama Server
   - Run the Ollama server locally to listen on the specified endpoint (http://localhost:11434).

**Installation**

**Install Dependencies**
1) The required Python packages can be installed using pip: pip install pynput pyperclip httpx

**Usage**
1) Start the script by running:
   - python summarize.py

2) Using Hotkeys
   - F9 Key: Summarizes the current line.
   - F10 Key: Summarizes the selected text.
When a hotkey is pressed, the script performs the following actions:

F9 Key:
Selects the entire current line.
Copies the selected text to the clipboard.
Sends the text to the Ollama server for summarization/grammar correction based on your requirement.
Replaces the original text with the updated version.

F10 Key:
Copies the selected text to the clipboard.
Sends the text to the Ollama server for summarization.
Replaces the original text with the summarized version.

**Notes**
Ensure that the Ollama server is running and accessible at the specified endpoint.
The project uses the pynput library for capturing global hotkeys and pyperclip for clipboard operations.
You may need to modify the hotkey bindings depending on your system and keyboard layout. 
Specifically for MAC system with ventura or later version you need to first disable your default input of F9 and F10 keys. Follow this link to diable https://support.apple.com/en-in/102439