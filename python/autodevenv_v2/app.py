import os
import random
import string
import re
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Carregar credenciais do arquivo .env
load_dotenv()

app = Flask(__name__)

access_token = os.environ.get("BITBUCKET_TOKEN")
workspace = os.environ.get("BITBUCKET_WORKSPACE")
repo_slug = os.environ.get("BITBUCKET_REPO_SLUG")

def generate_valid_suffix(length):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))

def is_valid_branch_name(name):
    return re.match(r'^[\w\-_]+$', name) and name not in ["master", "main"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_branch', methods=['POST'])
def create_branch():
    data = request.json
    prefix = data.get('prefix')
    branch_name = data.get('branchName')

    suffix = generate_valid_suffix(6)
    full_branch_name = f"{prefix}-{branch_name}-{suffix}"

    if not is_valid_branch_name(full_branch_name):
        return jsonify({"error": "Invalid branch name"}), 400

    api_url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/refs/branches"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "name": full_branch_name,
        "target": {
            "hash": os.environ.get("BITBUCKET_HASH"),
        }
    }

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 201:
        return jsonify({"message": f"Branch '{full_branch_name}' created successfully", "branchName": full_branch_name}), 201
    else:
        return jsonify({"error": response.text}), response.status_code

@app.route('/branches', methods=['GET'])
def list_branches():
    api_url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/refs/branches"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        branches = response.json().get('values', [])
        return jsonify({"branches": branches}), 200
    else:
        return jsonify({"error": response.text}), response.status_code

@app.route('/delete_branch', methods=['DELETE'])
def delete_branch():
    data = request.json
    branch_name = data.get('branchName')

    if branch_name in ["main", "master"]:
        return jsonify({"error": "Cannot delete 'main' or 'master' branch"}), 400

    api_url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/refs/branches/{branch_name}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response
    response = requests.delete(api_url, headers=headers)
    if response.status_code == 204:
        return jsonify({"message": f"Branch '{branch_name}' deleted successfully"}), 200
    else:
        return jsonify({"error": response.text}), response.status_code

@app.route('/delete_all_branches', methods=['DELETE'])
def delete_all_branches():
    api_url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/refs/branches"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        return jsonify({"error": response.text}), response.status_code

    branches = response.json().get('values', [])
    branches_to_delete = [branch for branch in branches if branch['name'] not in ["main", "master"]]

    if not branches_to_delete:
        return jsonify({"message": "No branches to delete."}), 200

    errors = []
    for branch in branches_to_delete:
        branch_name = branch.get('name')
        if branch_name:
            delete_api_url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/refs/branches/{branch_name}"
            delete_response = requests.delete(delete_api_url, headers=headers)
            if delete_response.status_code != 204:
                errors.append({"branch": branch_name, "error": delete_response.text})

    if errors:
        return jsonify({"message": "Some branches could not be deleted", "errors": errors}), 207
    else:
        return jsonify({"message": "All branches deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
