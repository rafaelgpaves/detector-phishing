function isPhishingUrl(url) {
    const phishingIndicators = [
        "login", "update", "verify", "account", "security", "confirm"
    ];

    return phishingIndicators.some(indicator => url.includes(indicator));
}

function checkCurrentUrl() {
    const currentUrl = window.location.href;
    if (isPhishingUrl(currentUrl)) {
        alert("Cuidado!");
    }
}

document.addEventListener("DOMContentLoaded", checkCurrentUrl);
