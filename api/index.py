from flask import Flask, request, jsonify
from utils.transcript_utils import assemble_transcript
from utils.url_utils import validate_url
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

def validate_and_fetch_url(url):
    try:
        validated_url = validate_url(url)
        response = requests.get(validated_url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tag = soup.find('meta', {'name': 'grain:recording:json'})
        if not meta_tag or not meta_tag.get('content'):
            raise ValueError("JSON data not found in the page")
        
        json_data = json.loads(meta_tag['content'])
        return json_data
    except Exception as e:
        raise ValueError(f"Error fetching or parsing URL: {e}")

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

@app.route('/transcript/assemble', methods=['POST'])
def assemble_transcript_endpoint():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
        json_data = validate_and_fetch_url(url)
        transcript = assemble_transcript(json_data)
        return jsonify(transcript), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)