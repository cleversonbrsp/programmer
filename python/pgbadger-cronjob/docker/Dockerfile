FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

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

# Instala OCI CLI
RUN bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)" \
    -- --accept-all-defaults && \
    ln -s /root/bin/oci /usr/local/bin/oci

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY config.yaml /app/config.yaml

COPY download_and_convert.py .

CMD ["python", "download_and_convert.py"]
