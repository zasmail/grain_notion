import pytest
import json
from utils.transcript_utils import assemble_transcript

def test_assemble_transcript_success():
    json_data = {
        "transcript": {
            "data": {
                "speakerRanges": [
                    {"speakerId": "1", "startIndex": 0, "endIndex": 1, "startMs": 0, "endMs": 5000},
                    {"speakerId": "2", "startIndex": 2, "endIndex": 3, "startMs": 6000, "endMs": 10000}
                ],
                "results": [
                    [0, "Hello", 2500],
                    [2500, "world", 5000],
                    [6000, "Goodbye", 8000],
                    [8000, "world", 10000]
                ],
                "speakers": [
                    {"id": "1", "name": "John Doe"},
                    {"id": "2", "name": "Jane Smith"}
                ]
            }
        }
    }
    
    result = assemble_transcript(json_data)
    expected = [
        {"speaker": "John Doe", "speakerId": "1", "transcript": "Hello world", "startMs": 0, "endMs": 5000},
        {"speaker": "Jane Smith", "speakerId": "2", "transcript": "Goodbye world", "startMs": 6000, "endMs": 10000}
    ]
    assert result == expected

    # Write the result to a file
    with open('tests/sample_transcript_output.json', 'w') as f:
        json.dump(result, f, indent=4)

def test_assemble_transcript_empty():
    json_data = {
        "transcript": {
            "data": {
                "speakerRanges": [],
                "results": [],
                "speakers": []
            }
        }
    }
    
    result = assemble_transcript(json_data)
    assert result == []
