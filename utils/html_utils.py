import requests
from bs4 import BeautifulSoup
import json

def fetch_and_parse_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ConnectionError(f"Failed to fetch the page, status code: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    meta_tag = soup.find('meta', attrs={'name': 'grain:recording:json'})
    
    if not meta_tag or not meta_tag.get('content'):
        raise ValueError("Meta tag with name 'grain:recording:json' not found.")
    
    return json.loads(meta_tag['content']) 