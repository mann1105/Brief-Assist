document.getElementById('summarize-button').addEventListener('click', async () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.tabs.sendMessage(tabs[0].id, { action: 'summarize' }, async (response) => {
        if (response && response.text) {
          try {
            const summary = await summarizeText(response.text);
            document.getElementById('summary').textContent = summary;
          } catch (error) {
            console.error('Error:', error);
            document.getElementById('summary').textContent = 'An error occurred.';
          }
        }
      });
    });
  });
  