// Variables
const hostName = "com.auto_uncompress.host";

// Connection checker

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
let cooldown = false;

function checkConnection(callback) {
  console.log("Checking Connection...");
  if (cooldown) {
    console.log("Cooldown...");
    callback(false);
  }

  cooldown = true;
  delay(1000).then(() => {cooldown = false;});

  chrome.runtime.sendNativeMessage(hostName, {action: "ping"}, (response) => {
    if (chrome.runtime.lastError || !response) {
      console.error("Native host not found error: ", chrome.runtime.lastError);
      isConnected = false;
      updateConnectionUI(false);
      callback(false);
    } else if (response.status === "connected") {
      console.log("Chrome and native host are connected");
      updateConnectionUI(true);
      callback(true);
    } else {callback(false);}
  });
}

checkConnection(() => {})

// Download listener and unzip controller
console.log("Download listener started...");
chrome.downloads.onChanged.addListener((downloadDelta) => {
  if (downloadDelta.state && downloadDelta.state.current === "complete") {
    console.log("Download Complete");
    checkConnection((connected) => {
      if (!connected) {
        console.warn("Download finished, but native host is disconnected. Ignoring.");
        return;
      }
      chrome.downloads.search({ id: downloadDelta.id }, (results) => {
        if (results && results.length > 0) {
          const item = results[0];

          const extIndex = item.filename.lastIndexOf(".");
          const fileExtension = extIndex !== -1 ? item.filename.slice(extIndex).toLowerCase() : "";

          let payload = {
            action: "evaluate",
            filePath: item.filename,
            url: new URL(item.url || item.finalUrl).origin,
            fileType: fileExtension
          };

          console.log(payload);

          chrome.runtime.sendNativeMessage(hostName, payload, (response) => {
            if (chrome.runtime.lastError) {
              console.error("Native Messaging Error: " + chrome.runtime.lastError.message);
            } else {
              console.log("Result:", response);
            }
          });
        }
      });
    });
  }
});

// UI Controls
function updateConnectionUI(connected) {
  if (connected) {
    chrome.action.setBadgeText({ text: "ON" });
    chrome.action.setBadgeBackgroundColor({ color: "#28a745" });
    chrome.action.setTitle({ title: "Auto-Uncompress: Connected to Host" });
  } else {
    chrome.action.setBadgeText({ text: "OFF" });
    chrome.action.setBadgeBackgroundColor({ color: "#dc3545" });
    chrome.action.setTitle({ title: "Auto-Uncompress: Host not detected" });
  }
}