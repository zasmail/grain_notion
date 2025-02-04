from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

def validate_url(url):
    parsed_url = urlparse(url)
    if not parsed_url.netloc.endswith("grain.com"):
        raise ValueError("Invalid URL format for Grain recording.")
    
    # Ensure the path matches the expected format
    path_parts = parsed_url.path.split('/')
    if len(path_parts) < 4 or path_parts[1] != "share" or path_parts[2] != "recording":
        raise ValueError("Invalid URL format for Grain recording.")
    
    # Replace query with ?tab=transcript
    query = parse_qs(parsed_url.query)
    query['tab'] = ['transcript']
    new_query = urlencode(query, doseq=True)
    
    # Reconstruct the URL with the new query
    new_url = urlunparse(parsed_url._replace(query=new_query))
    return new_url 