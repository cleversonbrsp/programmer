from flask import Flask, request, render_template
import base64
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    image_data = data['image'].split(',')[1]
    location = data['location']

    # Salvar a imagem
    with open('captured_image.png', 'wb') as f:
        f.write(base64.b64decode(image_data))

    # Salvar a localização
    with open('location.txt', 'w') as f:
        f.write(f"Latitude: {location['latitude']}, Longitude: {location['longitude']}")

    return 'Success', 200

if __name__ == '__main__':
    app.run(debug=True)
