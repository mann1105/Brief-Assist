chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'fix-selection') {
      let selectedText = window.getSelection().toString();
      if (selectedText) {
        summarizeText(selectedText).then(summary => {
          showNotification("Summarized Text", summary);
        });
      }
    } else if (request.action === 'fix-current-line') {
      // Implement functionality for fixing the current line
    }
  });
  
  function showNotification(title, message) {
    chrome.notifications.create('', {
      type: 'basic',
      iconUrl: 'images/icon128.png',
      title: title,
      message: message
    });
  }
  