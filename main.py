import requests
import urllib.parse
import re
import string

# https://github.com/n0kovo/n0kovo_subdomains
with open("./n0kovo_subdomains_tiny.txt", "r") as f:
    SUBDOMAINS = list(map(lambda x: x.replace("\n", ""), f.readlines()))

# https://developers.google.com/safe-browsing/v4/get-started?hl=pt-br

# https://openphish.com/phishing_database.html
# https://github.com/openphish/pyopdb

# https://phishtank.org/api_info.php
# phishtank_url = "https://checkurl.phishtank.com/checkurl/"
# payload = {"url": url, "format": "json"}
# response = requests.post(phishtank_url, data=payload)
# print(response.content)
# print(response.headers)
# print(response.text)
# print(response.status_code)

def scan_url(url: str):
    print("Tentando encontrar subdomínios:")
    urls_encontradas = 0
    for sub in SUBDOMAINS:
        url = f"https://{sub}.{url}"
        try:
            requests.get(url)
            print(f"url encontrada ==> {url}")
            urls_encontradas += 1
        except:
            pass

    if urls_encontradas == 0:
        print("Nenhuma url encontrada")

url = input("Digite uma url para verificar: ")

regex = r".*(\!|@|#|\$|%|&|\*|\(|\))+.*"
print(re.search(regex, url))

numbers = {"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "8": "b"}
regex_numbers = r".*(0|1|3|4|5|7|8)+.*"
# print(re.search(regex_numbers, url))
if re.search(regex_numbers, url):
    url_sem_numeros = "".join(list(map(lambda x: numbers[x] if x in numbers else x, url)))
    print(url_sem_numeros)


