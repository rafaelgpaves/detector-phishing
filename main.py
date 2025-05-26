import os
import requests
import urllib.parse
import re
import string
from tqdm import tqdm
from dotenv import load_dotenv
import whois
from datetime import datetime
import json

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
            url = input("Insira uma url para analisar: ")

        if re.search(regex, url):
            print(f"Indício de phishing ==> {url} possui caracteres especiais")

    def numbers_analyzer(self):
        numbers = {"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "8": "b"}
        regex_numbers = r".*(0|1|3|4|5|7|8)+.*"

        url = self.domain
        if url is None:
            url = input("Insira uma url para analisar: ")

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
                # print(f"url encontrada ==> {url}")
                urls_encontradas += 1
            except:
                pass

        if urls_encontradas == 0:
            print("Nenhuma url encontrada")
        else:
            proporcao = urls_encontradas/escolha
            print(f"Foram encontrados {urls_encontradas} domínios (${100*proporcao:.2f}%)")

    def google_safe_browsing(self):
        key = os.getenv("GOOGLE_API_KEY")
        if key is None:
            print("Coloque uma chave da API google para testar esse serviço")
            return
        
        url = self.domain
        if url is None:
            url = input("Insira uma url para analisar: ")
        
        api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={key}"
        request_body = {
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

        response = requests.post(api_url, json=request_body)
        print(response.text)
    
    def idade_dominio(self):
        domain = self.domain
        if domain is None:
            domain = input("Insira uma url para analisar: ")

        w = whois.whois(domain)
        try:
            data = datetime.date(w["creation_date"][0])
        except:
            data = datetime.date(w["creation_date"])
        print(data)
    
    # outra possibilidade: modulo python (https://github.com/narbehaj/ssl-checker)
    def ssl_certificates(self):
        domain = self.domain
        if domain is None:
            domain = input("Insira uma url para analisar: ")

        api_url = f"https://ssl-checker.io/api/v1/check/{domain}"
        response = requests.get(api_url)
        response = json.loads(response.text)

        if response["status"] == "ok":
            print(f"Emissor: {response['result']['issuer_o']}")
            print(f"Data de expiração: {response['result']['valid_till']} (faltam {response['result']['valid_days_to_expire']} dias para expirar)")
            print(f"Emitido para: {response['result']['issued_to']}")

    # primeiro checar se todos os redirecionamentos tem mesmo dono
    def check_redirections(self):
        key = os.getenv("GOOGLE_API_KEY")
        if key is None:
            print("Coloque uma chave da API google para testar esse serviço")
            return
        
        domain = self.domain
        if domain is None:
            domain = input("Insira uma url para analisar: ")
        
        response = requests.get(domain, allow_redirects=True)
        urls = []
        organizations = []
        num_redirecionamentos_suspeitos = 0
        for resp in response.history:
            print(f"Redirecionando para {resp.url}...")
            urls.append(resp.url)
            w = whois.whois(resp.url)
            organizations.append(w["org"])
            if w["org"] != organizations[0]:
                print(f"{domain} da organização {organizations[0]} tem redirecionamento suspeito para {resp.url} da organização {w['org']}")
                num_redirecionamentos_suspeitos += 1

        if num_redirecionamentos_suspeitos == 0:
            print("Nenhum redirecionamento suspeito encontrado")

    def run(self):
        print("\n0. Sair")
        print("1. Escolher url")
        print("2. Procurar caracteres especiais")
        print("3. Procurar números")
        print("4. Subdominios")
        print("5. Google Safe Browsing")
        print("6. Idade do domínio (whois)")
        print("7. Analisar certificados SSL")
        print("8. Analisar redirecionamentos")
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

        elif escolha == "5":
            self.google_safe_browsing()

        elif escolha == "6":
            self.idade_dominio()

        elif escolha == "7":
            self.ssl_certificates()

        elif escolha == "8":
            self.check_redirections()

def main():
    load_dotenv()
    detector = Detector()
    while detector.running:
        try:
            detector.run()
        except Exception as e:
            print(f"Ocorreu uma exceção: {e}")
            print("Verifique o input esperado e tente novamente")

if __name__ == "__main__":
    main()
