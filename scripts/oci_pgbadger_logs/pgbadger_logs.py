#!/usr/bin/env python3

# Importações de bibliotecas necessárias
import oci                      # SDK da Oracle Cloud Infrastructure
import gzip                    # Para descompactar arquivos .gz
import shutil                  # Para manipulação de arquivos
import subprocess              # Para execução do comando pgbadger
import os                      # Para manipulação de variáveis de ambiente e arquivos
import time                    # Para cálculo de tempo de execução
from datetime import datetime, timezone  # Manipulação de datas em UTC
import re                      # Expressões regulares

# Dicionário com a configuração de cada ambiente mapeado por chave
# Contém o nome, bucket, namespace e caminhos de cada DB System
ENVIRONMENTS = {
    "0": {
        "name": "pg-connect-navita-allprod",
        "bucket": "log-postgresqldbsystem-prod",
        "namespace": "grsmpvipzqfz",
        "folder": "ocid1.postgresqldbsystem.oc1.iad.amaaaaaabfbxvlaane42hjiip3vczht4ihk6ucjmr2ceouneldd4g24t7sea",
        "subfolder": "ae96e428-e9a0-4835-80fa-eebc8ce69294"
    },
    "1": {
        "name": "pg-connect-vivo",
        "bucket": "log-postgresqldbsystem-prod",
        "namespace": "grsmpvipzqfz",
        "folder": "ocid1.postgresqldbsystem.oc1.iad.amaaaaaabfbxvlaawu2kr6rac2yaxqwl4bcqzcsbxvnza35cdw65r5wcmt6a",
        "subfolder": "f693af9f-944a-43e4-ab63-f92c06823265"
    },
    "2": {
        "name": "pg-connect-navita-hom-equalizacao",
        "bucket": "log-postgresqldbsystem-hom",
        "namespace": "grsmpvipzqfz",
        "folder": "ocid1.postgresqldbsystem.oc1.iad.amaaaaaabfbxvlaabrhiit44fiqncpr46g4faclq74fp755jr2l4qm45q23q",
        "subfolder": "846c4dd3-8ad1-49bc-be0a-ce3175c781af"
    },
    "3": {
        "name": "pg-connect-telefonica",
        "bucket": "log-postgresqldbsystem-prod",
        "namespace": "grsmpvipzqfz",
        "folder": "ocid1.postgresqldbsystem.oc1.iad.amaaaaaabfbxvlaa7ehzver2d6cuoevmhkxtvso5odkzlrkwyqutby7mvnaq",
        "subfolder": "655c5ffd-e06a-446f-9c5a-08da303cd833"
    }
}

# Converte string "YYYY-MM-DD HH:MM" para datetime UTC
def parse_datetime(dt_str):
    return datetime.strptime(dt_str, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)

# Extrai data/hora do log a partir do nome do arquivo usando regex
# Ex: postgresql-2025-06-18_040000.csv.gz
def extract_datetime_from_filename(filename):
    match = re.search(r'postgresql-(\d{4}-\d{2}-\d{2}_\d{6})', filename)
    if match:
        return datetime.strptime(match.group(1), "%Y-%m-%d_%H%M%S").replace(tzinfo=timezone.utc)
    return None

# Lista os objetos dentro do bucket no intervalo especificado
# Compara com base na data extraída do nome do arquivo
def get_objects_by_range(bucket_name, namespace, prefix, start_time, end_time):
    # Carrega a configuração OCI a partir de variáveis de ambiente
    config = oci.config.from_file()
    # config = {
    #     "user": os.environ["OCI_CLI_USER"],
    #     "tenancy": os.environ["OCI_CLI_TENANCY"],
    #     "fingerprint": os.environ["OCI_CLI_FINGERPRINT"],
    #     "key_content": os.environ["OCI_CLI_KEY_CONTENT"],
    #     "region": os.environ["OCI_CLI_REGION"]
    # }
    client = oci.object_storage.ObjectStorageClient(config)

    filtered = []       # Lista dos arquivos válidos encontrados
    next_token = None   # Token para paginação
    page = 1            # Contador de páginas para debug
    start_timer = time.time()  # Cronômetro para medir performance

    while True:
        # Paginação da API de listagem de objetos
        response = client.list_objects(
            namespace,
            bucket_name,
            prefix=prefix,
            start=next_token,
            fields="name"
        )
        objects = response.data.objects

        print(f"[*] Página {page}: {len(objects)} objeto(s) retornado(s).")
        for obj in objects:
            print(f"  - {obj.name}")
        page += 1

        for obj in objects:
            if not obj.name.endswith(".gz"):
                continue  # Ignora arquivos que não sejam gzipados
            log_time = extract_datetime_from_filename(obj.name)
            if log_time and start_time <= log_time <= end_time:
                filtered.append(obj.name)

        if not response.data.next_start_with:
            break  # Fim da paginação
        next_token = response.data.next_start_with

    duration = time.time() - start_timer
    print(f"[*] Busca concluída em {duration:.2f} segundos. Total de objetos filtrados: {len(filtered)}")
    return filtered

# Faz o download do objeto especificado do bucket para um diretório local
def download_object(bucket, namespace, name, dest):
    config = oci.config.from_file()
    # config = {
    #     "user": os.environ["OCI_CLI_USER"],
    #     "tenancy": os.environ["OCI_CLI_TENANCY"],
    #     "fingerprint": os.environ["OCI_CLI_FINGERPRINT"],
    #     "key_content": os.environ["OCI_CLI_KEY_CONTENT"],
    #     "region": os.environ["OCI_CLI_REGION"]
    # }
    client = oci.object_storage.ObjectStorageClient(config)
    r = client.get_object(namespace, bucket, name)
    os.makedirs(dest, exist_ok=True)
    local_path = os.path.join(dest, os.path.basename(name))
    with open(local_path, "wb") as f:
        shutil.copyfileobj(r.data.raw, f)
    return local_path

# Descompacta o arquivo .gz e retorna o caminho do arquivo extraído
def extract_gz(gz_path):
    out_path = gz_path.rstrip(".gz")
    with gzip.open(gz_path, 'rb') as f_in:
        with open(out_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return out_path

# Executa o pgbadger em um log único (não usado no final, mas útil para debug/testes isolados)
def run_pgbadger(log_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    out_html = os.path.join(output_dir, os.path.basename(log_path) + ".html")
    subprocess.run(["pgbadger", log_path, "-o", out_html], check=True)
    return out_html

# Função principal
def main():
    # Lê o ambiente e intervalo de tempo a partir das variáveis de ambiente
    env_key = os.environ["PG_ENV"]
    start = parse_datetime(os.environ["PG_START"])
    end = parse_datetime(os.environ["PG_END"])

    # Carrega as configurações do ambiente selecionado
    cfg = ENVIRONMENTS[env_key]
    prefix = f"{cfg['folder']}/{cfg['subfolder']}/"
    output_dir = "/home/cleverson/Downloads/tmp"

    # Informações iniciais
    print(f"[*] Ambiente: {cfg['name']}")
    print(f"[*] Intervalo: {start.strftime('%d/%m/%Y %H:%M')} até {end.strftime('%H:%M')} (UTC)")

    # Busca os objetos dentro do intervalo de tempo
    objects = get_objects_by_range(cfg["bucket"], cfg["namespace"], prefix, start, end)
    print(f"[*] {len(objects)} arquivo(s) encontrado(s) no intervalo especificado.")
    if not objects:
        print("[!] Nenhum log encontrado no intervalo.")
        return

    # Faz download e extração dos logs
    log_files = []
    for obj in objects:
        gz = download_object(cfg["bucket"], cfg["namespace"], obj, output_dir)
        log = extract_gz(gz)
        if log.endswith(".csv"):
            log_files.append(log)

    # Monta comando pgbadger unificado com todos os arquivos
    unified_output = os.path.join(output_dir, f"{cfg['name']}.html")
    pgbadger_cmd = [
        "pgbadger",
        "--prefix", "%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h",
        *log_files,
        "-o", unified_output
    ]
    print("[*] Executando:", " ".join(pgbadger_cmd))
    subprocess.run(pgbadger_cmd, check=True)
    print(f"[✓] Relatório unificado gerado: {unified_output}")


# Ponto de entrada do script
if __name__ == "__main__":
    main()
