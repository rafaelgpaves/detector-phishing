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
            chrome.storage.local.get(["whitelist"]).then((data) => {
                var whitelist = data.whitelist;
                var urls = result.urlsSuspeitas;
                if (urls.length == 0) {
                    chrome.storage.local.set({ "urlsSuspeitas" : [message.url]});
                }
                if (!whitelist?.includes(message.url)) {
                    if (urls.length > 0 && !urls.includes(message.url)) {
                        chrome.storage.local.set({ "urlsSuspeitas" : [...urls, message.url]});
                    }
                }
            });
        });
    }
});
