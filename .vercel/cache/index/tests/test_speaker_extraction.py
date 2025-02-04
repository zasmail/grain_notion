import pytest
from utils.speaker_utils import extract_speaker_data  # Assuming you create this function

def test_extract_speaker_data_success():
    json_data = {
        "transcript": {
            "data": {
                "speakers": [
                    {"id": "1", "name": "John Doe"},
                    {"id": "2", "name": "Jane Smith"}
                ]
            }
        }
    }
    
    result = extract_speaker_data(json_data)
    assert result == {"1": "John Doe", "2": "Jane Smith"}

def test_extract_speaker_data_missing():
    json_data = {
        "transcript": {
            "data": {
                "speakers": []
            }
        }
    }
    
    result = extract_speaker_data(json_data)
    assert result == {} 