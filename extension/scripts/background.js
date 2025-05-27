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
                console.log(urls)
                if (urls === undefined) {
                    chrome.storage.local.set({ "urlsSuspeitas" : []})
                }
                if (!whitelist?.includes(message.url)) {
                    if (urls?.length > 0 && !urls?.includes(message.url)) {
                        chrome.storage.local.set({ "urlsSuspeitas" : [...urls, message.url]});
                    } else if (urls?.length == 0) {
                        console.log(1)
                        chrome.storage.local.set({ "urlsSuspeitas" : [message.url]});
                    }
                }

                chrome.storage.local.get(["bloquear"]).then((resposta) => {
                    if (resposta.bloquear) {
                        var new_rules = []
                            urls?.forEach((url, idx) => {
                            let id = idx + 1;
                            new_rules.push({
                                "id": id,
                                "priority": 1,
                                "action": { "type": "block" },
                                "condition": {
                                    "urlFilter": `|${url}`,
                                    "resourceTypes": ["main_frame"]
                                }
                            })
                        });
                        chrome.declarativeNetRequest.getDynamicRules(previousRules => {
                            const previousRuleIds = previousRules.map(rule => rule.id);
                            chrome.declarativeNetRequest.updateDynamicRules({
                                removeRuleIds: previousRuleIds,
                                addRules: new_rules
                            });
                        });
                    } else {
                        chrome.declarativeNetRequest.getDynamicRules(previousRules => {
                            const previousRuleIds = previousRules.map(rule => rule.id);
                            chrome.declarativeNetRequest.updateDynamicRules({
                                removeRuleIds: previousRuleIds
                            });
                        });
                    }                    
                })
            });
        });
    }
});
