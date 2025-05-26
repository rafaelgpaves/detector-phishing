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