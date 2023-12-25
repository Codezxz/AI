chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    if (message.action === "sendData") {
      let xhr = new XMLHttpRequest();
      xhr.open("POST", "http://localhost:5000/", true);
      xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
      xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
          sendResponse({ response: xhr.responseText });
        }
      };
      xhr.send("data=" + encodeURIComponent(message.data));
      return true; // Needed for asynchronous response
    }
  });