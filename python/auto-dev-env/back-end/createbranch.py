import os
import random
import string
import re
import requests
import json
from dotenv import load_dotenv

# Carregar credenciais do arquivo .env
load_dotenv()

# Definir variáveis a partir das variáveis de ambiente
access_token = os.environ.get("BITBUCKET_TOKEN")
workspace = os.environ.get("BITBUCKET_WORKSPACE")
repo_slug = os.environ.get("BITBUCKET_REPO_SLUG")

# URL da API para criar branches
api_url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/refs/branches"

def generate_valid_suffix(length):
    # Gerar um sufixo aleatório usando apenas letras minúsculas
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))

# Solicitar ao usuário o prefixo da branch
while True:
    prefix = input("Escolha um prefixo para a branch (por exemplo, dev, prd, hml): ")
    if prefix in ["dev", "prd", "hml"]:
        break
    else:
        print("Prefixo inválido. Por favor, tente novamente.")

# Solicitar ao usuário o nome da nova branch
branch_name = input("Digite o nome da nova branch: ")

# Gerar o sufixo aleatório
suffix = generate_valid_suffix(6)

# Nome completo da branch
full_branch_name = f"{prefix}-{branch_name}-{suffix}"

# Validar nome da branch
def is_valid_branch_name(name):
    # Verificar caracteres permitidos e nomes reservados
    return re.match(r'^[\w\-_]+$', name) and name not in ["master", "main"]

# Garantir que o nome da branch seja válido
while not is_valid_branch_name(full_branch_name):
    print(f"O nome sugerido '{full_branch_name}' é inválido.")
    branch_name = input("Digite um nome alternativo para a branch: ")
    full_branch_name = f"{prefix}-{branch_name}-{suffix}"

# Definir cabeçalhos para a requisição da API
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}

# Definir o payload para criar a branch
payload = {
    "name": full_branch_name,
    "target": {
        "hash": os.environ.get("BITBUCKET_HASH"), # hash específico do commit ou branch base
    }
}

# Fazer a requisição para criar a branch
response = requests.post(api_url, headers=headers, json=payload)

# Verificar o status da resposta e imprimir o resultado
if response.status_code == 201:
    print(f"Branch '{full_branch_name}' criada com sucesso.")
    print(json.dumps(response.json(), sort_keys=True, indent=4, separators=(",", ": ")))
else:
    print(f"Falha ao criar a branch. Código de status: {response.status_code}")
    print(response.text)
