document.addEventListener("mouseover", async function (event) {
    const target = event.target;

    if (target.tagName === "A" && target.href) {
        const url = target.href;

        const isPhishing = await isPhishingURL(url);
        // console.log(isPhishing);
        if (isPhishing) {
            chrome.storage.local.get(["whitelist"]).then((data) => {
                const whitelist = data.whitelist;
                if (!whitelist?.includes(url)) {
                    chrome.runtime.sendMessage({ action: "openPopup" , url: url});
                }
            })
        }
    }
});

async function checkURL() {
    const url = window.location.href;
    // console.log(url)

    const isPhishing = await isPhishingURL(url);
    // console.log(isPhishing);
    if (isPhishing) {
        chrome.storage.local.get(["whitelist"]).then((data) => {
            const whitelist = data.whitelist;
            if (!whitelist?.includes(url)) {
                chrome.runtime.sendMessage({ action: "openPopup" , url: url});
            }
        })
    }
}
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", checkURL);
} else {
    checkURL();
}

async function isPhishingURL(url) {
//   return url.includes("stackoverflow.com"); // para teste
    const key = undefined; // COLOQUE SUA CHAVE AQUI
    if (key === undefined) {
        return false;
    }

    const api_url = `https://safebrowsing.googleapis.com/v4/threatMatches:find?key=${key}`
    const request_body = {
        "client": {
            "clientId": "projetodetectorphishing",
            "clientVersion": "1.4"
        },
        "threatInfo": {
            "threatTypes": ["SOCIAL_ENGINEERING", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["CHROME", "WINDOWS"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }

    const response = await fetch(api_url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(request_body)
    });

    const data = await response.json()
    // console.log(data);
    // console.log(data.matches, data.matches !== undefined)
    return data.matches !== undefined;
}
