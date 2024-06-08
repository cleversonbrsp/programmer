from flask import Flask, request, jsonify
from pytube import YouTube

app = Flask(__name__)

# Função para baixar o vídeo do YouTube
def download_video(url, output_path='C:/Users/cleve/Downloads'):
    try:
        yt = YouTube(url)
        # Obter o fluxo de maior resolução
        stream = yt.streams.get_highest_resolution()
        # Baixar o vídeo
        stream.download(output_path)
        return {"message": f"Download completo: {yt.title}"}
    except Exception as e:
        return {"error": f"Ocorreu um erro: {e}"}

@app.route('/download_video', methods=['POST'])
def handle_download():
    data = request.json
    video_url = data.get('videoUrl')
    if video_url:
        result = download_video(video_url)
        return jsonify(result)
    else:
        return jsonify({"error": "URL do vídeo não fornecida"}), 400

@app.route('/')
def index():
    # Renderizar a página HTML
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(debug=True)
