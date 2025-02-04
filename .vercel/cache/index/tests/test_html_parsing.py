import pytest
from utils.html_utils import fetch_and_parse_html  # Assuming you create this function

def test_fetch_and_parse_html_success(mocker):
    mock_response = '<html><head><meta name="grain:recording:json" content=\'{"transcript": {"data": {}}}\'></head></html>'
    mocker.patch('requests.get', return_value=mocker.Mock(status_code=200, text=mock_response))
    
    result = fetch_and_parse_html("https://grain.com/share/recording/recordingId/sessionId?tab=transcript")
    assert result == {"transcript": {"data": {}}}

def test_fetch_and_parse_html_no_meta(mocker):
    mock_response = '<html><head></head><body>No meta tag here</body></html>'
    mocker.patch('requests.get', return_value=mocker.Mock(status_code=200, text=mock_response))
    
    with pytest.raises(ValueError, match="Meta tag with name 'grain:recording:json' not found."):
        fetch_and_parse_html("https://grain.com/share/recording/recordingId/sessionId?tab=transcript") 