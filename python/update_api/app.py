import os
import subprocess
from flask import Flask, request, render_template, redirect, url_for, flash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

UPLOAD_FOLDER = '/path/to/uploaded/packages'
EXTRACT_FOLDER = '/path/to/extracted/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update', methods=['POST'])
def update():
    if 'package' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['package']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = 'update_package.zip'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        subprocess.run(['unzip', '-o', filepath, '-d', EXTRACT_FOLDER])

        # Executar backup
        subprocess.run(['bash', 'scripts/backup.sh'], env={
            'DB_USER': os.environ.get("DB_USER"),
            'DB_HOST': os.environ.get("DB_HOST"),
            'DB_NAME': os.environ.get("DB_NAME")
        })

        # Executar scripts de banco de dados
        subprocess.run(['bash', 'scripts/execute_scripts.sh'], env={
            'DB_USER': os.environ.get("DB_USER"),
            'DB_HOST': os.environ.get("DB_HOST"),
            'DB_NAME': os.environ.get("DB_NAME")
        })

        # Atualizar arquivos binários
        subprocess.run(['bash', 'scripts/update_binaries.sh'])

        # Verificação da atualização
        response = subprocess.run(['curl', '-s', 'http://yourwebsite.com/Help'], capture_output=True, text=True)
        if 'expected_version' in response.stdout:
            flash('Update successful')
        else:
            flash('Update failed, contact support')

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
