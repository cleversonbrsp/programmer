
"""
Script para:
1. Buscar logs `.gz` no Object Storage da OCI em um intervalo de tempo.
2. Baixar e descompactar os arquivos.
3. Rodar o pgbadger em cada log para gerar relatórios HTML.

Requisitos:
- pip install oci
- sudo apt install pgbadger

ps: os arquivos .html gerados pelo pgbadger serão armazenados localmente no runner, dentro do diretório /tmp/pgbadger-output.

Para teste local:
export PG_ENV=3
export PG_START="2025-06-18 04:00"
export PG_END="2025-06-18 05:00" # padrao para pegar apenas 1 arquivo no ambiente vivo
config = oci.config.from_file()
"""