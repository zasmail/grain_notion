import pytest
from unittest.mock import patch
from api.index import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_assemble_transcript_endpoint_success(client):
    url = "https://grain.com/share/recording/5241a92e-1ab8-47c8-8f54-ec9f3649eac5/5lcMmg64fZU5DziAUDsBuEANYo968z0e1rBiSHVi?tab=summary"
    
    # Mock the validate_and_fetch_url function to return a sample JSON
    sample_json = {
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
        },
        "intelligence": {
            "chapters": {
                "data": [{"title": "Introduction", "start": 0}]
            },
            "summaryTabSections": [
                {
                    "section": {"title": "Outcomes"},
                    "data": [{"outcome": "Achieve project goals"}]
                },
                {
                    "section": {"title": "Action Items"},
                    "data": [{"action": "Follow up with team"}]
                }
            ]
        }
    }
    
    with patch('api.index.validate_and_fetch_url', return_value=sample_json):
        response = client.post('/transcript/assemble', json={"url": url})
        assert response.status_code == 200
        assert response.json == {
            "transcript": [
                {"speaker": "John Doe", "speakerId": "1", "transcript": "Hello world", "startMs": 0, "endMs": 5000},
                {"speaker": "Jane Smith", "speakerId": "2", "transcript": "Goodbye world", "startMs": 6000, "endMs": 10000}
            ],
            "chapters": [{"title": "Introduction", "start": 0}],
            "outcomes": [{"outcome": "Achieve project goals"}],
            "action_items": [{"action": "Follow up with team"}]
        }

def test_assemble_transcript_endpoint_invalid_url(client):
    url = "invalid-url"
    
    response = client.post('/transcript/assemble', json={"url": url})
    assert response.status_code == 500
    assert "error" in response.json

def test_assemble_transcript_endpoint_missing_url(client):
    response = client.post('/transcript/assemble', json={})
    assert response.status_code == 400
    assert response.json == {"error": "URL is required"}

def test_assemble_transcript_endpoint_fetch_error(client):
    url = "https://grain.com/share/recording/invalid"
    
    with patch('api.index.validate_and_fetch_url', side_effect=ValueError("Error fetching or parsing URL")):
        response = client.post('/transcript/assemble', json={"url": url})
        assert response.status_code == 500
        assert "error" in response.json 