document.addEventListener("DOMContentLoaded", () => {
    chrome.storage.local.get("urlsSuspeitas", (data) => {
        const txt = document.getElementById("site");
        if (data.urlsSuspeitas) {
            txt.textContent = `${data.urlsSuspeitas} pode ser um phishing.`;
        } else {
            txt.textContent = "Nenhuma URL suspeita detectada.";
        }
    });
});