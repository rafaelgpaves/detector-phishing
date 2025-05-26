document.addEventListener('DOMContentLoaded', function() {
    const suspiciousLinks = ['youtube.com']; // Add more known phishing URLs here

    const links = document.getElementsByTagName('a');
    for (let link of links) {
        link.addEventListener('click', function(event) {
            const url = new URL(link.href);
            if (suspiciousLinks.includes(url.hostname)) {
                event.preventDefault();
                alert('Cuidado!');
            }
        });
    }
});

document.addEventListener("mouseover", function (event) {
  const target = event.target;

  if (target.tagName === "A" && target.href) {
    const url = target.href;

    // Verificar se o link é suspeito
    if (isPhishingURL(url)) {
        chrome.runtime.sendMessage({ action: "openPopup" , url: url});
    }
  }
});

function isPhishingURL(url) {
  return url.includes("youtube.com");
}
