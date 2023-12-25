chrome.runtime.onInstalled.addListener(function() {
    console.log('Service worker registered');
  });
  
  chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === "sendData") {
      fetch('http://localhost:5000/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'data=' + encodeURIComponent(message.data)
      })
        .then(response => response.json())
        .then(data => {
          sendResponse({ response: data.response });
        })
        .catch(error => {
          console.error('Error:', error);
          sendResponse({ error: error.message });
        });
      return true; // Needed for asynchronous response
    }
  });
  