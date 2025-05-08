import requests
import urllib.parse
import re
import string
from tqdm import tqdm

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

class Detector:
    def __init__(self):
        self.running = True

        self.domain = None

    def special_characters_analyzer(self):
        regex = r".*(\!|@|#|\$|%|&|\*|\(|\))+.*"

        url = self.domain
        if url is None:
            url = input("Insira um dominio para analisar: ")

        if re.search(regex, url):
            print(f"Indício de phishing ==> {url} possui caracteres especiais")

    def numbers_analyzer(self):
        numbers = {"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "8": "b"}
        regex_numbers = r".*(0|1|3|4|5|7|8)+.*"

        url = self.domain
        if url is None:
            url = input("Insira um dominio para analisar: ")

        if re.search(regex_numbers, url):
            print(f"Indício de phishing ==> {url} possui números. Verificando se existe uma url sem numeros:")
            url_sem_numeros = "".join(list(map(lambda x: numbers[x] if x in numbers else x, url)))
            try:
                requests.get(url_sem_numeros)
                print(f"Encontrada url {url} sem números: {url_sem_numeros}")
            except:
                pass

    def subdomain_scanner(self):
        escolha = ""
        while not escolha.isnumeric():
            print("Digite numero de subdominios para escanear ou 0 para voltar:")
            escolha = input(">>> ")
        escolha = int(escolha)
        if escolha == 0:
            return
        
        domain = self.domain
        if domain is None:
            domain = input("Insira um dominio para analisar: ")
        
        print("Tentando encontrar subdomínios:")
        urls_encontradas = 0    
        for i in tqdm(range(escolha)):
            url = f"https://{SUBDOMAINS[i]}.{domain}"
            try:
                requests.get(url)
                print(f"url encontrada ==> {url}")
                urls_encontradas += 1
            except:
                pass

        if urls_encontradas == 0:
            print("Nenhuma url encontrada")

    def run(self):
        print("\n0. Sair")
        print("1. Escolher url")
        print("2. Procurar caracteres especiais")
        print("3. Procurar numeros")
        print("4. Subdominios")
        escolha = input(">>> ")

        if escolha == "0":
            self.running = False

        elif escolha == "1":
            self.domain = input("Insira um dominio para analisar: ")

        elif escolha == "2":
            self.special_characters_analyzer()

        elif escolha == "3":
            self.numbers_analyzer()
        
        elif escolha == "4":
            self.subdomain_scanner()

def main():
    detector = Detector()
    while detector.running:
        detector.run()

if __name__ == "__main__":
    main()
