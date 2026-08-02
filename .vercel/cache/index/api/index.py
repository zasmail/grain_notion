import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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

def extract_metadata(json_data):
    try:
        intelligence = json_data.get('intelligence', {})
        
        chapters = intelligence.get('chapters', {}).get('data', [])
        
        outcomes = []
        action_items = []
        
        for section in intelligence.get('summaryTabSections', []):
            if section.get('section', {}).get('title') == 'Outcomes':
                outcomes = section.get('data', [])
            elif section.get('section', {}).get('title') == 'Action Items':
                action_items = section.get('data', [])
        
        return chapters, outcomes, action_items
    except KeyError as e:
        raise ValueError(f"Error extracting metadata: {e}")

def parse_participants(participants_str):
    """
    Parses a participants string into an array of participant dictionaries.

    Expected input example (as in docs/data_participants.json):
        "confirmed_attendee: False\n        email: eshan@cashmereai.com\n
         name: eshan\n        scope: external\n\n        confirmed_attendee: True\n 
         email: jakob@cashmereai.com\n        name: jakob\n        scope: external\n ... "

    Returns:
        An array of dictionaries, e.g.:
        {
          "confirmed": true,
          "email": "test@email",
          "name": "John Doe",
          "external": true
        }
    """
    # Split the string by double newlines into blocks for each participant.
    blocks = participants_str.strip().split("\n\n")
    participants = []
    for block in blocks:
        # Split block into individual lines and remove any extra spaces.
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        participant_dict = {}
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                participant_dict[key.strip()] = value.strip()
        # Map the keys to the desired output.
        confirmed = participant_dict.get("confirmed_attendee", "False").lower() == "true"
        email = participant_dict.get("email", "").strip()
        name = participant_dict.get("name", "").strip()
        scope_val = participant_dict.get("scope", "").strip().lower()
        external = (scope_val == "external")
        participants.append({
            "confirmed": confirmed,
            "email": email if email.lower() != "none" else None,
            "name": name,
            "external": external
        })
    return participants

def test_parse_participants():
    """
    Helper function to test parse_participants.
    It pulls the participants string from docs/data_participants.json,
    calls parse_participants, and prints the result.
    """
    # Adjust the path as needed; here, we assume docs is one level up.
    with open("../docs/data_participants.json", "r") as f:
        data = json.load(f)
    participants_str = data.get("participants", "")
    parsed = parse_participants(participants_str)
    from pprint import pprint
    print("Parsed Participants:")
    pprint(parsed)

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
        
        # An optional participants string is now expected.
        participants_str = data.get('participants', None)
        parsed_participants = []
        if participants_str:
            parsed_participants = parse_participants(participants_str)
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
        json_data = validate_and_fetch_url(url)
        transcript = assemble_transcript(json_data)
        chapters, outcomes, action_items = extract_metadata(json_data)
        
        response = {
            "chapters": chapters,
            "outcomes": outcomes,
            "action_items": action_items, 
            "transcript": transcript,
            "participants": parsed_participants
        }
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test_parse":
        test_parse_participants()
    else:
        app.run(debug=True)