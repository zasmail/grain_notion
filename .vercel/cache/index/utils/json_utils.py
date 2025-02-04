def parse_transcript_json(json_data):
    try:
        # Adjust this path based on the actual structure of your JSON
        if 'transcript' in json_data and 'data' in json_data['transcript']:
            transcript_data = json_data['transcript']['data']
            # Perform necessary parsing and extraction
            return transcript_data
        else:
            raise ValueError("Missing required transcript data.")
    except KeyError:
        raise ValueError("Missing required transcript data.") 