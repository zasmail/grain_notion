def extract_speaker_data(json_data):
    try:
        speakers = json_data['transcript']['data']['speakers']
        return {speaker['id']: speaker['name'] for speaker in speakers}
    except KeyError:
        raise ValueError("Missing required speaker data.") 