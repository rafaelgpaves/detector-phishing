# Detector Phishing

Feito para a Avaliação Final da disciplina de Tecnologias Hacker, 7° semestre da Engenharia de Computação do Insper

Esse projeto possui duas partes:
1. Detector de Phishing desenvolvido em Python
1. Extensão para Google Chrome desenvolvida em JavaScript

Antes de mais nada, clone o repositório:
```terminal
git clone https://github.com/rafaelgpaves/port-scanner-2.git
```

Para algumas funcionalidades, é requerida uma chave da API do Google Safe Browsing. Siga [este tutorial](https://developers.google.com/safe-browsing/v4/get-started) para criar a sua.

## Ferramenta de detecção desenvolvida em Python

### Como usar

Entre na pasta do repositório:
```terminal
cd port-scanner-2
```

É recomendado criar um env (opcional):
```terminal
python -m venv env
env/Scripts/activate
```

Instale as bibliotecas:
```terminal
pip install -r ./requirements.txt
```

Rode o aplicativo:
```terminal
python main.py
```

#### Para usar o Google Safe Browsing

Usando a chave da API:

Crie um arquivo .env (ou renomeie o .env.example para .env) e coloque sua chave da API no local indicado

### Funcionalidades

Foram feitas as seguintes funcionalidades:
- Verificação de se o domínio está em listas de phishing conhecidas (Google Safe Browsing). Isso requer uma chave da API
- Identificação da presença de números em substituição a letras no domínio
- Identificação do uso excessivo de subdomínios
- Identificação da presença de caracteres especiais na URL
- Análise idade do domínio através de consultas WHOIS
- Verificação de uso de DNS dinâmico
- Análise de certificados SSL (emissor, data de expiração, coincidência entre domínio e certificado)
- Detecção de redirecionamentos suspeitos

## Extensão de Google Chrome

### Como usar

1. Clique nos três círculos no canto superior direito do navegador. Selecione *extensões*, depois *gerir extensões*.
1. No canto superior direito, ative o *modo de desenvolvedor*.
1. No canto superior esquerdo, clique em *carregar expandida*. Navegue até a pasta *extension* clonada e clique em *selecionar pasta*

Ao entrar em um site suspeito, aparecerá automaticamente um popup.

Ao passar o mouse sobre um link suspeito, aparecerá automticamente um popup.

Caso você acredite que um site foi bloqueado sem razão, coloque-o na whitelist apertando no botão de *confiar neste site* no popup.

A princípio, o plugin não impede a navegação para páginas suspeitas. Para ativar essa opção, clique no ícone da extensão e ative a opção de bloquear sites suspeitos.

#### Para usar o Google Safe Browsing

Usando a chave da API:

Entre no arquivo *content.js*. Na linha 43, coloque sua chave.

Caso não queira fazer uma chave ou queira apenas testar, descomente a linha 42 de *content.js*. Isso simula como se o site "stackoverflow.com" fosse suspeito

### Funcionalidades

- Monitoramento ativo: Verificação de todas as páginas visitadas e links clicáveis em tempo real
- Notificações em tempo real: Alertas visuais quando uma página suspeita é detectada
- Bloqueio preventivo: Opção para bloquear automaticamente o acesso a páginas identificadas como phishing
- Personalização: Permitir que o usuário defina o nível de sensibilidade das análises e crie listas de sites confiáveis (whitelist)
- Análise de links: Verificação de links ao passar o mouse sobre eles antes mesmo de clicar
