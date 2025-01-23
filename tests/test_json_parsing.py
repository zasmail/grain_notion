import pytest
import json
from utils.json_utils import parse_transcript_json

def test_parse_transcript_json_success():
    with open('docs/meta_tag.json') as f:
        json_data = json.load(f)
    
    result = parse_transcript_json(json_data)
    assert result is not None  # Add more specific assertions based on expected output

def test_parse_transcript_json_missing_data():
    # Adjust this test data based on the actual structure
    json_data = {}  # Simulate missing data
    with pytest.raises(ValueError, match="Missing required transcript data."):
        parse_transcript_json(json_data) 