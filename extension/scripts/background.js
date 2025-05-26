chrome.action.onClicked.addListener((tab) => {
  chrome.scripting.executeScript({
    target: {tabId: tab.id},
    files: ['scripts/core.js']
  });
});

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "openPopup") {
        chrome.action.openPopup();
        chrome.storage.local.set({ "urlAtual" : message.url});
        chrome.storage.local.get(["urlsSuspeitas"]).then((result) => {
            var urls = result.urlsSuspeitas;
            if (urls.length > 0 && !urls.includes(message.url)) {
                chrome.storage.local.set({ "urlsSuspeitas" : [...urls, message.url]});
            } else {
                chrome.storage.local.set({ "urlsSuspeitas" : [message.url]});
            }
        });
    }
});
