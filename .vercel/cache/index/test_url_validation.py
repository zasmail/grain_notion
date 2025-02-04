import pytest
from url_utils import validate_url

def test_valid_url():
    url = "https://grain.com/share/recording/recordingId/sessionId?tab=summary"
    assert validate_url(url) == "https://grain.com/share/recording/recordingId/sessionId?tab=transcript"

def test_invalid_url():
    url = "https://invalid.com/share/recording/recordingId/sessionId"
    with pytest.raises(ValueError, match="Invalid URL format for Grain recording."):
        validate_url(url)

def test_url_without_query():
    url = "https://grain.com/share/recording/recordingId/sessionId"
    assert validate_url(url) == "https://grain.com/share/recording/recordingId/sessionId?tab=transcript" 