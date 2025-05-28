FROM python:3.13-slim

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Atualiza os pacotes e instala dependências + pgbadger direto do apt
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gzip \
    curl \
    make \
    perl \
    build-essential \
    git \
    pgbadger \
    && rm -rf /var/lib/apt/lists/*


# Cria diretório da aplicação
WORKDIR /app

# Copia arquivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY download_and_convert.py .

# Comando padrão
CMD ["python", "download_and_convert.py"]
