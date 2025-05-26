document.addEventListener("DOMContentLoaded", () => {
    chrome.storage.local.get("urlsSuspeitas", (data) => {
        const txt = document.getElementById("site");
        console.log(data.urlsSuspeitas);
        chrome.storage.local.get(["urlAtual"]).then((result) => {
            if (data.urlsSuspeitas && data.urlsSuspeitas.includes(result.urlAtual)) {
                txt.textContent = `${result.urlAtual} pode ser um phishing.`;
            } else {
                txt.textContent = "Nenhuma URL suspeita detectada.";
            }
        });
    });
});

function trustSite() {
    chrome.storage.local.get(["urlAtual"]).then((result) => {
        const url = result.urlAtual;
        chrome.storage.local.get(["whitelist"]).then((data) => {
            var whitelist = data.whitelist;
            if (whitelist?.length > 0 && !whitelist?.includes(url)) {
                chrome.storage.local.set({ "whitelist" : [...whitelist, url]});
            } else if (whitelist.length == 0) {
                chrome.storage.local.set({ "whitelist" : [url]});
            }
            console.log(whitelist);

            // Tirando url da lista de urls suspeitas
            chrome.storage.local.get(["urlsSuspeitas"]).then((response) => {
                var new_urls = response.urlsSuspeitas;
                const index = new_urls.indexOf(url);
                if (index > -1) {
                    new_urls.splice(index, 1);
                }
                console.log(new_urls);
                chrome.storage.local.set({ "urlsSuspeitas" : [...new_urls]});

                // Tirando regra para bloquear
                var new_rules = []
                new_urls.forEach((url, idx) => {
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
            })
        });
        alert(`Você não será mais avisado sobre ${url}`);
    });
}
document.getElementById("trust").addEventListener("click", trustSite)
