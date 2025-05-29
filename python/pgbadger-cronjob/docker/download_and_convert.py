#!/usr/bin/env python3
#
# Script: download_and_convert.py
# Descrição: Faz o download do arquivo .gz mais recente de um bucket na Oracle Cloud (OCI),
#            descompacta o arquivo CSV e gera um relatório HTML usando o pgBadger.
#
# Requisitos:
#   - Configuração válida no arquivo ~/.oci/config
#   - SDK da Oracle OCI instalado (oci)
#   - pgBadger instalado e acessível no PATH
#
# Autor: Cleverson (DevOps Engineer)
# Data de criação: 26/05/2025
# Versão: 1.0
#
#
# Observação:
#   Certifique-se de que o bucket contenha arquivos .csv.gz válidos gerados a partir dos logs do PostgreSQL.

#!/usr/bin/env python3
import oci
import gzip
import shutil
import subprocess
import os
import yaml

CONFIG_PATH = "/app/config.yaml"

def load_config():
    with open(CONFIG_PATH, 'r') as file:
        return yaml.safe_load(file)

def get_latest_object(bucket_name, namespace, object_storage):
    objects = object_storage.list_objects(namespace, bucket_name).data.objects
    if not objects:
        raise Exception("Nenhum objeto encontrado no bucket.")

    enriched_objects = []
    for obj in objects:
        if obj.name.endswith(".gz"):
            metadata = object_storage.head_object(namespace, bucket_name, obj.name)
            enriched_objects.append({
                "name": obj.name,
                "time_created": metadata.headers.get("last-modified")
            })

    from email.utils import parsedate_to_datetime
    enriched_objects = [
        {**obj, "dt": parsedate_to_datetime(obj["time_created"])}
        for obj in enriched_objects if obj["time_created"]
    ]

    latest = max(enriched_objects, key=lambda x: x["dt"])
    print(f"[+] Último objeto: {latest['name']} ({latest['time_created']})")
    return latest["name"]

def download_object(bucket_name, namespace, object_name, destination, object_storage):
    os.makedirs(destination, exist_ok=True)
    response = object_storage.get_object(namespace, bucket_name, object_name)

    local_path = os.path.join(destination, os.path.basename(object_name))
    with open(local_path, 'wb') as f:
        shutil.copyfileobj(response.data.raw, f)

    print(f"[+] Download: {local_path}")
    return local_path

def extract_gz(gz_path):
    csv_path = gz_path.rstrip(".gz")
    with gzip.open(gz_path, 'rb') as f_in:
        with open(csv_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"[+] Extraído: {csv_path}")
    return csv_path

def run_pgbadger(csv_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    output_html = os.path.join(output_dir, "report.html")
    subprocess.run(["pgbadger", csv_file, "-o", output_html], check=True)
    print(f"[+] Relatório: {output_html}")
    return output_html

def upload_report(report_path, bucket_name, namespace, target_path, object_storage):
    with open(report_path, 'rb') as f:
        object_storage.put_object(namespace, bucket_name, target_path, f)
    print(f"[✓] Upload para o bucket como {target_path}")

def main():
    print("[*] Iniciando...")

    cfg = load_config()
    config = oci.config.from_file()
    object_storage = oci.object_storage.ObjectStorageClient(config)

    latest = get_latest_object(cfg['bucket_name'], cfg['namespace'], object_storage)
    gz_path = download_object(cfg['bucket_name'], cfg['namespace'], latest, cfg['output_dir'], object_storage)
    csv_path = extract_gz(gz_path)
    html_path = run_pgbadger(csv_path, cfg['output_dir'])

    if cfg.get('upload_report'):
        upload_report(
            html_path,
            cfg['bucket_name'],
            cfg['namespace'],
            cfg.get('report_target_path', "relatorio/report.html"),
            object_storage
        )

    print("[✓] Finalizado com sucesso.")

if __name__ == "__main__":
    main()
