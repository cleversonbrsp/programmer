# ==========================================================================
# Script para Criar uma Branch no Bitbucket
# Criado por: Cleverson Rodrigues
# Data: 05/06/2024
# Descrição: Este script cria uma branch específica de um repositório no
#            Bitbucket usando a API do Bitbucket.
# ==========================================================================

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

def suggest_branch_name(suffix):
    # Gerar um sufixo aleatório (garantir caracteres válidos)
    def generate_valid_suffix(length):
        suffix = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
        valid_chars = re.sub(r'[^\w\-_]', '', suffix)
        return valid_chars[:length]

    suffix = generate_valid_suffix(6)
    return f"{prefix}-{suffix}"

# Solicitar ao usuário o prefixo da branch
while True:
    prefix = input("Escolha um prefixo para a branch (por exemplo, dev, prd, hml): ")
    if prefix in ["dev", "prd", "hml"]:
        break
    else:
        print("Prefixo inválido. Por favor, tente novamente.")

# Gerar o nome sugerido
branch_name = suggest_branch_name(prefix)

# Solicitar ao usuário o nome da nova branch
branch_name = input("Digite o nome da nova branch: ")

# Validar nome da branch (opcional)
def is_valid_branch_name(name):
    # Verificar caracteres permitidos e nomes reservados (ajustar conforme necessário)
    return re.match(r'^[\w\-_]+$', name) and name not in ["master", "main"]

# Garantir que o nome da branch seja válido
while not is_valid_branch_name(branch_name):
    print(f"O nome sugerido '{branch_name}' é inválido.")
    branch_name = input("Digite um nome alternativo para a branch: ")

# Nome completo da branch (validado ou sugerido)
full_branch_name = branch_name

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
