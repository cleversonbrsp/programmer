FROM python:3.11-slim

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema e pgBadger
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gzip \
    curl \
    make \
    perl \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Instala pgBadger
RUN git clone https://github.com/darold/pgbadger.git /opt/pgbadger && \
    cd /opt/pgbadger && \
    make && make install

# Cria diretório da aplicação
WORKDIR /app

# Copia arquivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY download_and_convert.py .

# Comando padrão
CMD ["python", "download_and_convert.py"]
