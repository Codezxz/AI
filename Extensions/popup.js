function sendData() {
    let userInput = document.getElementById("userInput").value;
    chrome.runtime.sendMessage({ action: "sendData", data: userInput }, function (
      response
    ) {
      console.log(response.response);
      document.getElementById("response").innerHTML = response.response;
    });
  }
  
  document.getElementById("sendBtn").addEventListener("click", sendData);