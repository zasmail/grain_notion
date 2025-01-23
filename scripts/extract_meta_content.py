import requests
from bs4 import BeautifulSoup
import json

def fetch_meta_content(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ConnectionError(f"Failed to fetch the page, status code: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    meta_tag = soup.find('meta', attrs={'name': 'grain:recording:json'})
    
    if not meta_tag or not meta_tag.get('content'):
        raise ValueError("Meta tag with name 'grain:recording:json' not found.")
    
    return json.loads(meta_tag['content'])

def save_json_to_file(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    url = "https://grain.com/share/recording/5241a92e-1ab8-47c8-8f54-ec9f3649eac5/5lcMmg64fZU5DziAUDsBuEANYo968z0e1rBiSHVi?tab=transcript"
    try:
        meta_content = fetch_meta_content(url)
        save_json_to_file(meta_content, 'docs/meta_tag.json')
        print("Meta content successfully saved to docs/meta_tag.json")
    except Exception as e:
        print(f"An error occurred: {e}") 