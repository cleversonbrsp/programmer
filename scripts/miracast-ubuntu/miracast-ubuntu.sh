#!/bin/bash

set -e

echo "[+] Verificando permissões..."
if [[ "$EUID" -ne 0 ]]; then
  echo "[-] Este script precisa ser executado como root (sudo)."
  exit 1
fi

echo "[+] Atualizando pacotes..."
apt update

echo "[+] Instalando dependências..."
apt install -y \
  build-essential \
  pkg-config \
  libsystemd-dev \
  libreadline-dev \
  libudev-dev \
  libtool \
  libdbus-1-dev \
  libglib2.0-dev \
  libnl-3-dev \
  libnl-genl-3-dev \
  libjson-glib-dev \
  git \
  cmake

echo "[+] Clonando o repositório miraclecast..."
cd /opt
if [[ ! -d miraclecast ]]; then
  git clone https://github.com/albfan/miraclecast.git
fi
cd miraclecast

echo "[+] Compilando o miraclecast..."
mkdir -p build && cd build
cmake ..
make
make install

echo "[+] Parando serviços antigos, se existirem..."
pkill -f miracle-wifid || true
pkill -f miracle-sinkctl || true

echo "[+] Iniciando o serviço miracle-wifid..."
miracle-wifid &
sleep 3

echo "[+] Detectando interfaces Wi-Fi compatíveis..."
INTERFACE_LINE=$(miracle-wifidctl list | grep -m1 -E "^[*]?[[:space:]]*[0-9]+:")

if [[ -z "$INTERFACE_LINE" ]]; then
  echo "[-] Nenhuma interface Wi-Fi Direct compatível encontrada."
  exit 1
fi

INTERFACE_ID=$(echo "$INTERFACE_LINE" | grep -oP '^[*]?\s*\K[0-9]+')

echo "[+] Interface selecionada: $INTERFACE_ID"

echo "[+] Iniciando transmissão Miracast (modo emissor)..."

miracle-wifidctl <<EOF
select $INTERFACE_ID
run 1
EOF
