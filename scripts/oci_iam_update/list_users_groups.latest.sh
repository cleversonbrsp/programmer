#!/bin/bash

################################################################################
# Script: list_users_groups.latest.sh
# Autor: Cleverson
# Descrição:
#   Este script automatiza a listagem de usuários da Oracle Cloud Infrastructure (OCI),
#   coleta os grupos aos quais cada usuário pertence e atualiza o campo "description"
#   do usuário com os nomes dos grupos. Além disso, salva um resumo no arquivo
#   'user_groups.txt' contendo o nome de cada usuário e seus respectivos grupos.
#
# Requisitos:
#   - OCI CLI instalado e configurado
#   - jq instalado
#
# Funcionalidades:
#   - Lista todos os usuários do tenancy
#   - Para cada usuário:
#     - Obtém os grupos aos quais pertence
#     - Atualiza o campo "description" com os grupos
#     - Registra o resultado em 'user_groups.txt'
#
# Uso:
#   ./list_users_groups.latest.sh
#
# Observações:
#   - O script assume que a região default da CLI é apropriada,
#     ou então utiliza explicitamente "--region gru" na atualização.
################################################################################


#!/bin/bash

# Arquivo de saída
output_file="user_groups.txt"

# Limpa o arquivo de saída
> "$output_file"

# Lista todos os usuários na OCI
user_ocids=$(oci iam user list --query "data[*].id" --output json | jq -r '.[]')

if [ -z "$user_ocids" ]; then
  echo "Nenhum usuário encontrado."
  exit 1
fi

# Para cada usuário, lista os grupos e escreve no arquivo de saída e atualiza o description
for user_ocid in $user_ocids; do
  echo "-----------------------------------------------------------"

  # Obtém o nome do usuário
  user_name=$(oci iam user get --user-id "$user_ocid" --query "data.\"name\"" --output json | jq -r '.')

  if [ -z "$user_name" ]; then
    echo "Nome do usuário não encontrado para OCID: $user_ocid"
    continue
  fi

  # Obtém os grupos
  groups=$(oci iam user list-groups --user-id "$user_ocid" --query "data[*].name" --output json | jq -r '.[]' | paste -s -d, -)
  [ -z "$groups" ] && groups="Sem grupos"

  # Atualiza o description do usuário
  oci iam user update \
    --user-id "$user_ocid" \
    --description "Grupos: $groups" \
    --region gru > /dev/null

  # Exibe saída clean
  echo "Usuário: $user_name"
  echo "Grupos: $groups"
  echo "Description atualizado com sucesso."

  # Salva no arquivo de saída
  echo "Usuário: $user_name | Grupos: $groups" >> "$output_file"
done

# Exibe o conteúdo do arquivo
echo "-----------------------------------------------------------"
echo "Resumo salvo em: $output_file"
