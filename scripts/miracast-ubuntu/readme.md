Claro, Cleverson. Abaixo está a documentação completa, organizada e estruturada, cobrindo todo o processo para preparar seu Ubuntu para transmitir a tela via Miracast usando Miraclecast, desde instalação até conexão à TV.

---

# Transmitir Tela Ubuntu para TV via Miracast com Miraclecast

---

## 1. Introdução

Miracast é uma tecnologia para espelhamento de tela sem fio via Wi-Fi Direct (P2P). No Ubuntu, o suporte oficial é limitado, mas podemos usar o projeto **Miraclecast** para implementar esse recurso.

Essa documentação orienta a instalação, configuração e uso do Miraclecast para transmitir a tela do Ubuntu para uma TV compatível com Miracast.

---

## 2. Requisitos

* **Hardware:**

  * Placa Wi-Fi que suporte Wi-Fi Direct (P2P). Pode ser verificado com `iw list`.
* **Software:**

  * Ubuntu (testado em versões recentes).
  * `wpa_supplicant` compilado com suporte a P2P (`CONFIG_P2P=y`).
  * Miraclecast compilado e instalado.

---

## 3. Verificação da Placa Wi-Fi para P2P

No terminal, rode:

```bash
iw list | grep -A 10 "Supported interface modes"
```

Procure por:

```
* P2P-client
* P2P-GO
* P2P-device
```

Se esses modos existirem, sua placa suporta Wi-Fi Direct.

---

## 4. Preparação do Sistema

### 4.1 Instalar dependências básicas

```bash
sudo apt update
sudo apt install -y build-essential pkg-config libsystemd-dev libreadline-dev \
libudev-dev libtool libdbus-1-dev libglib2.0-dev libnl-3-dev libnl-genl-3-dev \
libjson-glib-dev git cmake
```

---

### 4.2 Compilar e instalar o `wpa_supplicant` com suporte P2P (se necessário)

Se o `wpa_supplicant` atual não suportar P2P, compile assim:

```bash
cd /tmp
wget https://w1.fi/releases/wpa_supplicant-2.10.tar.gz
tar zxvf wpa_supplicant-2.10.tar.gz
cd wpa_supplicant-2.10/wpa_supplicant

vim defconfig
# Adicione ou descomente:
# CONFIG_P2P=y
# Salve e saia (:wq)

make
sudo make install

sudo systemctl stop wpa_supplicant.service
sudo killall wpa_supplicant
```

---

## 5. Clonar, compilar e instalar Miraclecast

### 5.1 Clonar o repositório

```bash
cd /opt
sudo git clone https://github.com/albfan/miraclecast.git
sudo chown -R $USER:$USER miraclecast
cd miraclecast
```

### 5.2 Compilar

```bash
mkdir -p build && cd build
cmake ..
make
```

### 5.3 Copiar binários para `/usr/local/bin`

```bash
sudo cp src/wifi/miracle-wifid /usr/local/bin/
sudo cp src/ctl/miracle-wifictl /usr/local/bin/
sudo cp src/ctl/miracle-sinkctl /usr/local/bin/
sudo cp src/miracled /usr/local/bin/
sudo chmod +x /usr/local/bin/miracle-*
```

---

## 6. Uso do Miraclecast para transmitir a tela

### 6.1 Iniciar o daemon miracle-wifid

```bash
sudo /usr/local/bin/miracle-wifid &
sleep 3
```

### 6.2 Listar interfaces Wi-Fi compatíveis

```bash
sudo /usr/local/bin/miracle-wifictl list
```

Anote o número da interface Wi-Fi que você vai usar (ex: 1).

### 6.3 Conectar e transmitir (modo emissor/source)

```bash
sudo /usr/local/bin/miracle-wifictl
```

No prompt interativo:

```
select 1      # substitua 1 pelo ID da sua interface
run 1         # inicia a transmissão no modo emissor (source)
```

### 6.4 Na TV

* Ative o modo **Screen Mirroring** ou similar.
* Selecione seu notebook na lista de dispositivos.
* Aceite a conexão.

---

## 7. Parar a transmissão

No prompt do `miracle-wifictl`, digite:

```
stop
exit
```

---

## 8. Dicas e Observações

* Se aparecer o aviso:

```
WARNING: supplicant: wpa_supplicant or driver does not support P2P
```

significa que o suporte Wi-Fi Direct está faltando no `wpa_supplicant` ou no driver Wi-Fi.

* Verifique que não haja gerenciadores de rede interferindo (ex: NetworkManager pode precisar ser configurado para não bloquear Wi-Fi Direct).

* Para automatizar a conexão, é possível criar scripts que executem os comandos interativos.

---

## 9. Exemplo de script básico para iniciar a conexão

```bash
#!/bin/bash
sudo /usr/local/bin/miracle-wifid &
sleep 3

INTERFACE_ID=$(sudo /usr/local/bin/miracle-wifictl list | grep -m1 -E "^[*]?[[:space:]]*[0-9]+:" | grep -oP '^[*]?\s*\K[0-9]+')

if [ -z "$INTERFACE_ID" ]; then
  echo "Nenhuma interface Wi-Fi Direct compatível encontrada."
  exit 1
fi

echo "Usando interface $INTERFACE_ID"

sudo /usr/local/bin/miracle-wifictl <<EOF
select $INTERFACE_ID
run 1
EOF
```

---
