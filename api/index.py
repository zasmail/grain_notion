from flask import Flask, request, jsonify
from url_utils import validate_url

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/validate-url', methods=['POST'])
def validate_url_route():
    data = request.get_json()
    url = data.get('url')
    try:
        validated_url = validate_url(url)
        return jsonify({"validated_url": validated_url}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400