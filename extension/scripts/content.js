document.addEventListener("mouseover", function (event) {
    const target = event.target;

    if (target.tagName === "A" && target.href) {
        const url = target.href;

        if (isPhishingURL(url)) {
            chrome.storage.local.get(["whitelist"]).then((data) => {
                const whitelist = data.whitelist;
                if (!whitelist?.includes(url)) {
                    chrome.runtime.sendMessage({ action: "openPopup" , url: url});
                }
            })
        }
    }
});

function checkURL() {
    const url = window.location.href;
    console.log(url)

    if (isPhishingURL(url)) {
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

function isPhishingURL(url) {
  return url.includes("stackoverflow.com");
}
