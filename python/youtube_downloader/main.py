import yt_dlp
import os

def escolher_caminho():
    caminho = input("Dê um nome para a pasta de destino: ").strip() # Enter para padrão
    if not caminho:
        caminho = os.path.expanduser("/home/cleverson/Downloads") # Diretório padrão. Altere para o seu.
    if not os.path.exists(caminho):
        print(f"O caminho '{caminho}' não existe. Criando...")
        os.makedirs(caminho)
    return caminho

def baixar_video(url, output_path):
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': False
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def baixar_audio(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def baixar_playlist(url, output_path, modo):
    if modo == 'video':
        ydl_opts = {
            'outtmpl': f'{output_path}/%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'quiet': False,
            'yes_playlist': True
        }
    else:
        ydl_opts = {
            'outtmpl': f'{output_path}/%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': False,
            'yes_playlist': True
        }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def baixar_legendas(url, output_path):
    idioma = input("Digite o código do idioma da legenda (ex: pt, en): ").strip() or 'pt'
    usar_auto = input("Usar legenda automática? [s/N]: ").strip().lower()
    auto_sub = True if usar_auto == 's' else False

    ydl_opts = {
        'skip_download': True,
        'writesubtitles': not auto_sub,
        'writeautomaticsub': auto_sub,
        'subtitleslangs': [idioma],
        'subtitlesformat': 'srt',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'quiet': False
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\nBaixando apenas legenda ({'automática' if auto_sub else 'manual'}) em '{idioma}'...")
            ydl.download([url])
            print("\n✅ Legenda baixada com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro ao baixar legenda: {e}")

def menu():
    print("\n=== YouTube Downloader ===")
    print("[1] Baixar vídeo (.mp4)")
    print("[2] Baixar áudio (.mp3)")
    print("[3] Baixar playlist de vídeos (.mp4)")
    print("[4] Baixar playlist de áudios (.mp3)")
    print("[5] Baixar apenas as legendas")
    print("[6] Sair")

if __name__ == "__main__":
    while True:
        menu()
        escolha = input("Escolha uma opção [1-6]: ").strip()

        if escolha == '6':
            print("Encerrando.")
            break

        url = input("Digite a URL do vídeo ou playlist: ").strip()
        caminho = escolher_caminho()

        if escolha == '1':
            baixar_video(url, caminho)
        elif escolha == '2':
            baixar_audio(url, caminho)
        elif escolha == '3':
            baixar_playlist(url, caminho, modo='video')
        elif escolha == '4':
            baixar_playlist(url, caminho, modo='audio')
        elif escolha == '5':
            baixar_legendas(url, caminho)
        else:
            print("❌ Opção inválida.")
