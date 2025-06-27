#!/usr/bin/env python3
# =============================================================================
# SCRIPT PGBADGER LOGS ANALYZER - ORACLE CLOUD INFRASTRUCTURE
# =============================================================================
# Este script automatiza a análise de logs PostgreSQL armazenados no OCI
# Object Storage. Ele busca logs em um intervalo de tempo específico,
# baixa e descompacta os arquivos, e gera relatórios HTML usando PGBadger.
# =============================================================================

# =============================================================================
# IMPORTAÇÕES DE BIBLIOTECAS NECESSÁRIAS
# =============================================================================
# Cada biblioteca tem um propósito específico no funcionamento do script
import oci                      # SDK da Oracle Cloud Infrastructure - para conectar ao OCI Object Storage
import gzip                    # Para descompactar arquivos .gz (logs comprimidos)
import shutil                  # Para manipulação de arquivos (cópia, criação de diretórios)
import subprocess              # Para execução do comando pgbadger no sistema
import os                      # Para manipulação de variáveis de ambiente e operações de arquivo
import time                    # Para cálculo de tempo de execução e performance
from datetime import datetime, timezone  # Manipulação de datas em UTC (padrão OCI)
import re                      # Expressões regulares para extrair datas dos nomes de arquivo

# =============================================================================
# CONFIGURAÇÃO DE AMBIENTES
# =============================================================================
# Dicionário com a configuração de cada ambiente mapeado por chave
# Contém o nome, bucket, namespace e caminhos de cada DB System
# Cada ambiente representa um banco de dados PostgreSQL diferente no OCI
ENVIRONMENTS = {
    # Ambiente 0 - Primeiro banco de dados
    "0": {
        "name": "nome-do-ambiente-0",                    # Nome amigável do ambiente
        "bucket": "nome-do-bucket-0",                    # Nome do bucket no OCI Object Storage
        "namespace": "nome-do-namespace",                # Namespace do tenancy OCI
        "folder": "nome-do-folder(normalmente o OCID do DB System)",      # Pasta principal (geralmente OCID do DB System)
        "subfolder": "nome-do-subfolder(normalmente um UUID sistemico)"   # Subpasta (geralmente UUID do sistema)
    },
    # Ambiente 1 - Segundo banco de dados
    "1": {
        "name": "nome-do-ambiente-1",
        "bucket": "nome-do-bucket-1",
        "namespace": "nome-do-namespace",
        "folder": "nome-do-folder(normalmente o OCID do DB System)",
        "subfolder": "nome-do-subfolder(normalmente um UUID sistemico)"
    },
    # Ambiente 2 - Terceiro banco de dados
    "2": {
        "name": "nome-do-ambiente-2",
        "bucket": "nome-do-bucket-2",
        "namespace": "nome-do-namespace",
        "folder": "nome-do-folder(normalmente o OCID do DB System)",
        "subfolder": "nome-do-subfolder(normalmente um UUID sistemico)"
    },
    # Ambiente 3 - Quarto banco de dados
    "3": {
        "name": "nome-do-ambiente-3",
        "bucket": "nome-do-bucket-3",
        "namespace": "nome-do-namespace",
        "folder": "nome-do-folder(normalmente o OCID do DB System)",
        "subfolder": "nome-do-subfolder(normalmente um UUID sistemico)"
    }
}

# =============================================================================
# FUNÇÕES AUXILIARES PARA MANIPULAÇÃO DE DATAS
# =============================================================================

def parse_datetime(dt_str):
    """
    Converte string "YYYY-MM-DD HH:MM" para datetime UTC
    Exemplo: "2025-06-18 04:00" -> datetime(2025, 6, 18, 4, 0, tzinfo=timezone.utc)
    """
    return datetime.strptime(dt_str, "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)

def extract_datetime_from_filename(filename):
    """
    Extrai data/hora do log a partir do nome do arquivo usando regex
    Exemplo: postgresql-2025-06-18_040000.csv.gz -> datetime(2025, 6, 18, 4, 0, 0, tzinfo=timezone.utc)
    
    Padrão esperado: postgresql-YYYY-MM-DD_HHMMSS.csv.gz
    """
    match = re.search(r'postgresql-(\d{4}-\d{2}-\d{2}_\d{6})', filename)
    if match:
        return datetime.strptime(match.group(1), "%Y-%m-%d_%H%M%S").replace(tzinfo=timezone.utc)
    return None

# =============================================================================
# FUNÇÕES PRINCIPAIS PARA INTERAÇÃO COM OCI OBJECT STORAGE
# =============================================================================

def get_objects_by_range(bucket_name, namespace, prefix, start_time, end_time):
    """
    Lista os objetos dentro do bucket no intervalo especificado
    Compara com base na data extraída do nome do arquivo
    
    Parâmetros:
    - bucket_name: Nome do bucket no OCI
    - namespace: Namespace do tenancy
    - prefix: Prefixo do caminho (pasta/subpasta)
    - start_time: Data/hora de início (datetime UTC)
    - end_time: Data/hora de fim (datetime UTC)
    
    Retorna: Lista com nomes dos arquivos que estão no intervalo especificado
    """
    # Carrega a configuração OCI a partir do arquivo de configuração padrão
    # Alternativamente, pode usar variáveis de ambiente (comentado abaixo)
    # config = oci.config.from_file() # Para uso local
    config = {
        "user": os.environ["OCI_CLI_USER"],
        "tenancy": os.environ["OCI_CLI_TENANCY"],
        "fingerprint": os.environ["OCI_CLI_FINGERPRINT"],
        "key_content": os.environ["OCI_CLI_KEY_CONTENT"],
        "region": os.environ["OCI_CLI_REGION"]
    }
    
    # Cria cliente para interagir com o Object Storage
    client = oci.object_storage.ObjectStorageClient(config)

    # Variáveis para controle da busca e paginação
    filtered = []       # Lista dos arquivos válidos encontrados
    next_token = None   # Token para paginação (quando há muitos objetos)
    page = 1            # Contador de páginas para debug
    start_timer = time.time()  # Cronômetro para medir performance

    # Loop de paginação - busca todos os objetos em lotes
    while True:
        # Faz a requisição para a API do OCI Object Storage
        # fields="name" retorna apenas os nomes dos objetos (economiza banda)
        response = client.list_objects(
            namespace,
            bucket_name,
            prefix=prefix,
            start=next_token,
            fields="name"
        )
        objects = response.data.objects

        # Log de debug - mostra quantos objetos foram retornados nesta página
        print(f"[*] Página {page}: {len(objects)} objeto(s) retornado(s).")
        for obj in objects:
            print(f"  - {obj.name}")
        page += 1

        # Filtra os objetos desta página
        for obj in objects:
            # Ignora arquivos que não sejam gzipados (só processa .gz)
            if not obj.name.endswith(".gz"):
                continue
            
            # Extrai a data do nome do arquivo
            log_time = extract_datetime_from_filename(obj.name)
            
            # Verifica se está no intervalo de tempo especificado
            if log_time and start_time <= log_time <= end_time:
                filtered.append(obj.name)

        # Verifica se há mais páginas para buscar
        if not response.data.next_start_with:
            break  # Fim da paginação
        next_token = response.data.next_start_with

    # Log final com estatísticas de performance
    duration = time.time() - start_timer
    print(f"[*] Busca concluída em {duration:.2f} segundos. Total de objetos filtrados: {len(filtered)}")
    return filtered

def download_object(bucket, namespace, name, dest):
    """
    Faz o download do objeto especificado do bucket para um diretório local
    
    Parâmetros:
    - bucket: Nome do bucket
    - namespace: Namespace do tenancy
    - name: Nome do objeto no bucket
    - dest: Diretório local onde salvar o arquivo
    
    Retorna: Caminho local do arquivo baixado
    """
    # Configuração OCI (mesma lógica da função anterior)
    # config = oci.config.from_file() # Para uso local
    config = {
        "user": os.environ["OCI_CLI_USER"],
        "tenancy": os.environ["OCI_CLI_TENANCY"],
        "fingerprint": os.environ["OCI_CLI_FINGERPRINT"],
        "key_content": os.environ["OCI_CLI_KEY_CONTENT"],
        "region": os.environ["OCI_CLI_REGION"]
    }
    
    # Cria cliente e faz o download do objeto
    client = oci.object_storage.ObjectStorageClient(config)
    r = client.get_object(namespace, bucket, name)
    
    # Cria o diretório de destino se não existir
    os.makedirs(dest, exist_ok=True)
    
    # Define o caminho local do arquivo
    local_path = os.path.join(dest, os.path.basename(name))
    
    # Salva o arquivo localmente
    with open(local_path, "wb") as f:
        shutil.copyfileobj(r.data.raw, f)
    
    return local_path

# =============================================================================
# FUNÇÕES PARA PROCESSAMENTO DE ARQUIVOS
# =============================================================================

def extract_gz(gz_path):
    """
    Descompacta o arquivo .gz e retorna o caminho do arquivo extraído
    
    Parâmetros:
    - gz_path: Caminho do arquivo .gz
    
    Retorna: Caminho do arquivo extraído (sem a extensão .gz)
    """
    out_path = gz_path.rstrip(".gz")  # Remove a extensão .gz
    
    # Abre o arquivo gzip e extrai o conteúdo
    with gzip.open(gz_path, 'rb') as f_in:
        with open(out_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    return out_path

def run_pgbadger(log_path, output_dir):
    """
    Executa o pgbadger em um log único
    (não usado no final, mas útil para debug/testes isolados)
    
    Parâmetros:
    - log_path: Caminho do arquivo de log
    - output_dir: Diretório onde salvar o relatório HTML
    
    Retorna: Caminho do arquivo HTML gerado
    """
    os.makedirs(output_dir, exist_ok=True)
    out_html = os.path.join(output_dir, os.path.basename(log_path) + ".html")
    
    # Executa o comando pgbadger
    subprocess.run(["pgbadger", log_path, "-o", out_html], check=True)
    
    return out_html

# =============================================================================
# FUNÇÃO PRINCIPAL - ORQUESTRA TODO O PROCESSO
# =============================================================================

def main():
    """
    Função principal que orquestra todo o processo:
    1. Lê configurações das variáveis de ambiente
    2. Busca logs no intervalo especificado
    3. Baixa e extrai os arquivos
    4. Executa PGBadger para gerar relatório unificado
    """
    
    # =====================================================================
    # ETAPA 1: LEITURA DE CONFIGURAÇÕES
    # =====================================================================
    # Lê o ambiente e intervalo de tempo a partir das variáveis de ambiente
    env_key = os.environ["PG_ENV"]           # Qual ambiente usar (0, 1, 2, ou 3)
    start = parse_datetime(os.environ["PG_START"])  # Data/hora de início
    end = parse_datetime(os.environ["PG_END"])      # Data/hora de fim

    # Carrega as configurações do ambiente selecionado
    cfg = ENVIRONMENTS[env_key]
    prefix = f"{cfg['folder']}/{cfg['subfolder']}/"  # Caminho completo no bucket
    output_dir = "/tmp/pgbadger"     # Diretório local para salvar arquivos

    # Exibe informações iniciais para o usuário
    print(f"[*] Ambiente: {cfg['name']}")
    print(f"[*] Intervalo: {start.strftime('%d/%m/%Y %H:%M')} até {end.strftime('%H:%M')} (UTC)")

    # =====================================================================
    # ETAPA 2: BUSCA DE LOGS NO OCI OBJECT STORAGE
    # =====================================================================
    # Busca os objetos dentro do intervalo de tempo especificado
    objects = get_objects_by_range(cfg["bucket"], cfg["namespace"], prefix, start, end)
    print(f"[*] {len(objects)} arquivo(s) encontrado(s) no intervalo especificado.")
    
    # Verifica se encontrou algum log
    if not objects:
        print("[!] Nenhum log encontrado no intervalo.")
        return

    # =====================================================================
    # ETAPA 3: DOWNLOAD E EXTRAÇÃO DOS LOGS
    # =====================================================================
    # Faz download e extração dos logs encontrados
    log_files = []  # Lista para armazenar caminhos dos arquivos de log extraídos
    
    for obj in objects:
        # Baixa o arquivo .gz do OCI
        gz = download_object(cfg["bucket"], cfg["namespace"], obj, output_dir)
        
        # Extrai o arquivo .gz
        log = extract_gz(gz)
        
        # Adiciona à lista apenas se for um arquivo CSV (log PostgreSQL)
        if log.endswith(".csv"):
            log_files.append(log)

    # =====================================================================
    # ETAPA 4: GERAÇÃO DO RELATÓRIO UNIFICADO COM PGBADGER
    # =====================================================================
    # Monta comando pgbadger unificado com todos os arquivos
    unified_output = os.path.join(output_dir, f"{cfg['name']}.html")
    
    # Comando pgbadger com parâmetros:
    # --prefix: Define o formato do log PostgreSQL
    # *log_files: Lista de todos os arquivos de log
    # -o: Arquivo de saída HTML
    pgbadger_cmd = [
        "pgbadger",
        "--prefix", "%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h",
        *log_files,
        "-o", unified_output
    ]
    
    # Executa o comando pgbadger
    print("[*] Executando:", " ".join(pgbadger_cmd))
    subprocess.run(pgbadger_cmd, check=True)
    
    # Confirmação de sucesso
    print(f"[✓] Relatório unificado gerado: {unified_output}")

# =============================================================================
# PONTO DE ENTRADA DO SCRIPT
# =============================================================================
# Garante que o script só execute se for chamado diretamente
# (não se for importado como módulo)
if __name__ == "__main__":
    main()
