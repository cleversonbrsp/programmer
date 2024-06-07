import os
import requests
from dotenv import load_dotenv

# Carregar credenciais do arquivo .env
load_dotenv()

# Definir variáveis a partir das variáveis de ambiente
access_token = os.environ.get("BITBUCKET_TOKEN")
workspace = os.environ.get("BITBUCKET_WORKSPACE")
repo_slug = os.environ.get("BITBUCKET_REPO_SLUG")

# Solicitar ao usuário o nome da branch a ser excluída
branch_name = input("Digite o nome da branch que deseja excluir: ")

# URL da API para excluir branches
api_url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/refs/branches/{branch_name}"

# Definir cabeçalhos para a requisição da API
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}

# Fazer a requisição para excluir a branch
response = requests.delete(api_url, headers=headers)

# Verificar o status da resposta e imprimir o resultado
if response.status_code == 204:
    print(f"Branch '{branch_name}' excluída com sucesso.")
elif response.status_code == 404:
    print(f"Branch '{branch_name}' não encontrada.")
else:
    print(f"Falha ao excluir a branch. Código de status: {response.status_code}")
    print(response.text)
