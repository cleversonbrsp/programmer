# 📄 Documentação: YouTube Downloader CLI com `yt-dlp`

## 🧾 Visão Geral

Este script Python fornece uma interface de linha de comando interativa para baixar vídeos, áudios, playlists e **legendas** do YouTube. Utiliza `yt-dlp`, uma poderosa ferramenta baseada no `youtube-dl`, com suporte a `ffmpeg` para mesclar ou converter arquivos multimídia.

---

## 🚀 Funcionalidades

* ✅ Baixar vídeo completo em `.mp4` (melhor qualidade disponível)
* ✅ Baixar apenas o áudio em `.mp3`
* ✅ Baixar playlists completas (vídeo ou áudio)
* ✅ Baixar **apenas legendas** (manual ou automática) em qualquer idioma
* ✅ Escolha do diretório de destino para cada operação

---

## 🧱 Requisitos

### Python 3.7 ou superior

### Bibliotecas Python:

```bash
pip install yt-dlp
```

### ffmpeg:

#### Ubuntu/Debian:

```bash
sudo apt update
sudo apt install ffmpeg
```

#### Fedora:

```bash
sudo dnf install ffmpeg
```

---

## 📂 Estrutura do Projeto

```
youtube_downloader/
│
├── main.py         # Script principal com menu interativo
└── README.md       # (opcional) Documentação do projeto
```

---

## ▶️ Como Executar

```bash
python3 main.py
```

---

## 📜 Menu de Opções

Ao iniciar o script, você verá:

```
=== YouTube Downloader ===
[1] Baixar vídeo (.mp4)
[2] Baixar áudio (.mp3)
[3] Baixar playlist de vídeos (.mp4)
[4] Baixar playlist de áudios (.mp3)
[5] Baixar apenas as legendas
[6] Sair
```

Você escolhe uma opção, fornece a URL do vídeo ou playlist, e informa (ou confirma) o diretório de destino.

---

## 📝 Detalhes das Opções

### `[1] Baixar vídeo (.mp4)`

* Faz o download do vídeo em alta qualidade (vídeo + áudio).
* Salva como `.mp4` usando `ffmpeg` para mesclar.

### `[2] Baixar áudio (.mp3)`

* Extrai apenas o áudio do vídeo.
* Converte para `.mp3` via `ffmpeg`.

### `[3] Baixar playlist de vídeos`

* Baixa todos os vídeos da playlist.
* Os arquivos são organizados por pasta com título da playlist.

### `[4] Baixar playlist de áudios`

* Extrai apenas os áudios de toda a playlist.
* Salva como `.mp3`.

### `[5] Baixar apenas as legendas`

* Permite selecionar o idioma (ex: `pt`, `en`, `es`).
* Escolher entre legenda **manual** ou **automática**.
* Salva como `.srt`.

---

## 📦 Exemplos de Uso

### Baixar legenda automática em português:

```
Escolha: 5
URL: https://www.youtube.com/watch?v=O2onA5sHZgI
Idioma: pt
Usar legenda automática? s
```

### Baixar playlist de áudios:

```
Escolha: 4
URL: https://www.youtube.com/playlist?list=...
```

---

## 📁 Organização dos arquivos

* Arquivos de vídeo ou áudio são salvos com o nome do título do vídeo.
* Playlists são salvas em pastas nomeadas com o título da playlist.
* Legendas são salvas como `titulo-do-video.srt`.

---

## 🔒 Permissões

Certifique-se de ter permissões de gravação no diretório de destino escolhido.

---

## 💡 Expansões Futuras (sugestões)

* Interface gráfica com Tkinter ou PyQt
* Conversão de `.srt` para `.txt`
* Embutir legenda no vídeo com `ffmpeg`
* Suporte a múltiplas plataformas (Vimeo, TikTok, etc.)
* Exportar metadados em `.json` ou `.csv`
* Automatizar download de novos vídeos de um canal (RSS/watch later)

---

## 👨‍💻 Autor

**Cleverson**
DevOps Engineer | Automação | Observabilidade | Cloud OCI