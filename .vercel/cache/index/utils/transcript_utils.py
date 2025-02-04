import pdb

def assemble_transcript(json_data):
    try:
        data = json_data['transcript']['data']
        speaker_ranges = data['speakerRanges']
        results = data['results']
        speakers = {speaker['id']: speaker['name'] for speaker in data['speakers']}
        
        transcript_segments = []
        for speaker_range in speaker_ranges:
            words = []
            start_index = speaker_range['startIndex']
            end_index = speaker_range['endIndex']
            
            # Initialize start and end times
            start_ms = None
            end_ms = None
            
            # Iterate over results with their index
            for idx, result in enumerate(results):
                if start_index <= idx <= end_index:
                    current_start_ms, word, current_end_ms = result
                    words.append(word)
                    
                    # Set start_ms if it's not set yet
                    if start_ms is None:
                        start_ms = current_start_ms
                    # Update end_ms to the current result's end time
                    end_ms = current_end_ms
            # pdb.set_trace()
            transcript_segments.append({
                "speaker": speakers.get(speaker_range['speakerId'], "Unknown Speaker"),
                "speakerId": speaker_range['speakerId'],
                "transcript": " ".join(words),
                "startMs": start_ms,
                "endMs": end_ms
            })
        
        return transcript_segments
    except KeyError as e:
        raise ValueError(f"Missing required transcript data: {e}") 