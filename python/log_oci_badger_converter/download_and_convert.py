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

import oci
import gzip
import shutil
import subprocess
import os

BUCKET_NAME = "log-postgresqldbsystem-hom"  # Substitua pelo nome real do bucket
NAMESPACE = "grsmpvipzqfz"  # Substitua pelo namespace real
OUTPUT_DIR = "/app/output" # Substitua pelo diretório de saída desejado

def get_latest_object(bucket_name, namespace):
    config = oci.config.from_file()
    object_storage = oci.object_storage.ObjectStorageClient(config)

    # Lista objetos (sem time_created confiável)
    objects = object_storage.list_objects(namespace, bucket_name).data.objects
    if not objects:
        raise Exception("Nenhum objeto encontrado no bucket.")

    # Lista com metadados reais
    enriched_objects = []
    for obj in objects:
        if obj.name.endswith(".gz"):
            metadata = object_storage.head_object(namespace, bucket_name, obj.name)
            enriched_objects.append({
                "name": obj.name,
                "time_created": metadata.headers.get("last-modified")  # em string RFC822
            })

    if not enriched_objects:
        raise Exception("Nenhum arquivo .gz encontrado.")

    # Ordenar por data
    from email.utils import parsedate_to_datetime
    enriched_objects = [
        {**obj, "dt": parsedate_to_datetime(obj["time_created"])}
        for obj in enriched_objects if obj["time_created"]
    ]

    if not enriched_objects:
        raise Exception("Nenhum .gz com metadata válida.")

    latest = max(enriched_objects, key=lambda x: x["dt"])
    print(f"[+] Último objeto encontrado: {latest['name']} ({latest['time_created']})")
    return latest["name"]

def download_object(bucket_name, namespace, object_name, destination):
    object_storage = oci.object_storage.ObjectStorageClient(oci.config.from_file())
    response = object_storage.get_object(namespace, bucket_name, object_name)

    os.makedirs(destination, exist_ok=True)
    local_gz_path = os.path.join(destination, os.path.basename(object_name))

    with open(local_gz_path, 'wb') as f:
        shutil.copyfileobj(response.data.raw, f)

    print(f"[+] Download concluído: {local_gz_path}")
    return local_gz_path

def extract_gz(gz_path):
    csv_path = gz_path.rstrip(".gz")
    with gzip.open(gz_path, 'rb') as f_in:
        with open(csv_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    print(f"[+] Arquivo extraído: {csv_path}")
    return csv_path

def run_pgbadger(csv_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    output_html = os.path.join(output_dir, "report.html")

    cmd = ["pgbadger", csv_file, "-o", output_html]
    subprocess.run(cmd, check=True)

    print(f"[+] Relatório gerado: {output_html}")
    return output_html

def main():
    print("[*] Iniciando script...")
    latest_object = get_latest_object(BUCKET_NAME, NAMESPACE)
    gz_path = download_object(BUCKET_NAME, NAMESPACE, latest_object, OUTPUT_DIR)
    csv_path = extract_gz(gz_path)
    html_report = run_pgbadger(csv_path, OUTPUT_DIR)
    print(f"[✓] Processo finalizado com sucesso: {html_report}")

if __name__ == "__main__":
    main()