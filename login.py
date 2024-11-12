import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Carrega as variáveis de ambiente
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
USER = os.getenv("USER")

# URL de login da API do Kaggle
login_url = 'https://www.kaggle.com/api/i/users.LegacyUsersService/EmailSignIn'
edit_url = "https://www.kaggle.com/code/{USER}/exercise-syntax-variables-and-numbers/edit"

# Inicializando a sessão
session = requests.Session()

# Primeiro, acessa a página inicial para obter os cookies e o XSRF token
initial_response = session.get("https://www.kaggle.com/account/login")

# Extraindo o XSRF Token dos cookies
xsrf_token = session.cookies.get('XSRF-TOKEN')

# Caso o XSRF Token não esteja presente nos cookies, procuramos no conteúdo HTML
if not xsrf_token:
    soup = BeautifulSoup(initial_response.text, 'html.parser')
    xsrf_token_tag = soup.find('input', {'name': 'X-XSRF-TOKEN'})
    if xsrf_token_tag:
        xsrf_token = xsrf_token_tag['value']

if not xsrf_token:
    raise Exception("Não foi possível encontrar o XSRF Token.")

# Dados para o login
login_data = {
    'email': EMAIL,
    'password': PASSWORD,
    'returnUrl': "/{USER}"
}

# Cabeçalhos da requisição
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
    'Content-Type': 'application/json',
    'X-XSRF-TOKEN': xsrf_token  # Adiciona o XSRF Token no cabeçalho
}

# Realizando o login
login_response = session.post(login_url, json=login_data, headers=headers)

# Verificando a resposta do servidor
if login_response.status_code == 200:
    print("[OK] Login realizado com sucesso.")

    # Acessando a URL específica
    edit_response = session.get(edit_url, headers=headers)

    if edit_response.status_code == 200:
        print("[OK] Página de edição acessada com sucesso.")
        # Exibe parte do conteúdo da página para verificação
        # print(edit_response.text)
    else:
        print(f"[ERROR] Erro ao acessar a página de edição. Status Code: {edit_response.status_code}")
        print(edit_response.text)  # Mostra uma parte da mensagem de erro para depuração
else:
    print(f"[ERROR] Falha ao realizar o login. Status Code: {login_response.status_code}")
    print(f"Mensagem de erro: {login_response.text}")
