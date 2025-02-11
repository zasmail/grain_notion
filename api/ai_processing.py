from flask import Flask, request, jsonify
import json
import os
import anthropic
from pprint import pprint
import pdb; 

app = Flask(__name__)

# Initialize Anthropic client; the API key is retrieved from environment variables,
# falling back to the provided key for demonstration purposes.
ANTHROPIC_API_KEY = os.environ.get(
    "ANTHROPIC_API_KEY",
    "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"
)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def load_prompts():
    """
    Loads the AI prompts and schemas from docs/ai_prompts_v0.json.
    Returns a dictionary keyed by prompt type (e.g., "tldr", "Action Items", etc.).
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    prompts_path = os.path.join(base_dir, '..', 'docs', 'ai_prompts_v0.json')
    
    with open(prompts_path, 'r') as f:
        data = json.load(f)

    return data

def call_anthropic_api(client, prompt):
    """
    Calls the Anthropics API using the specified model and prompt text.
    Returns the parsed JSON content from the first TextBlock of the response,
    or an empty dict if there's an issue.
    """
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    if response and hasattr(response, 'content') and len(response.content) > 0:
        # We assume content is a list of text blocks
        try:
            raw_text = response.content[0].text
            return json.loads(raw_text)  # Convert from JSON string to dict
        except (json.JSONDecodeError, AttributeError, IndexError):
            # If parsing fails or content is unexpected, return an empty dict
            return {}
    else:
        return {}

def process_ai_requests(client, prompt_keys, transcript_text):
    """
    Takes a list of prompt keys (e.g., ["tldr", "measurableBuisnessImpacts"]) and the transcript text.
    1. Loads prompt definitions and output schemas from ai_prompts_v0.json.
    2. For each key, retrieves the prompt template and schema.
    3. Calls the Anthropics API.
    4. Parses the JSON response and adds it to a results array.

    :param client: Anthropics client instance.
    :param prompt_keys: List of strings corresponding to keys in ai_prompts_v0.json (e.g., ["tldr", "Action Items"]).
    :param transcript_text: The joined transcript string.
    :return: A list of dicts, each containing {"promptKey": <key>, "result": <parsed AI response>}.
    """
    if not transcript_text.strip():
        raise ValueError("Transcript text is empty.")

    # Load the prompts/ schemas
    prompts_data = load_prompts()
    
    # Prepare a list to store all the responses
    results = []

    for key in prompt_keys:
        # Retrieve prompt info from the JSON
        if key not in prompts_data:
            # If the key isn't in our AI prompts file, skip or handle error
            results.append({
                "promptKey": key,
                "error": f"Prompt key '{key}' not found in ai_prompts_v0.json."
            })
            continue
        
        # Build the prompt text
        prompt_info = prompts_data[key]
        prompt_template = prompt_info.get("prompt", "")
        
        # (Optional) We can display or use output_schema from prompt_info.get("output_schema")
        # if we want to dynamically handle or validate the returned structure.

        # Combine the template with transcript
        # Here, we simply append the transcript to the prompt:
        full_prompt = (
            f"{prompt_template}\n\n"
            f"Please return the answer in valid JSON matching "
            f"this schema:\n{prompt_info.get('output_schema', {})}\n\n"
            f"{transcript_text}"
        )

        # Call Anthropics
        ai_response = call_anthropic_api(client, full_prompt)

        # Add to results
        results.append({
            "promptKey": key,
            "result": ai_response
        })

    return results

def main_logic(client, data):
    """
    Example function that demonstrates how you might use `process_ai_requests`.
    This snippet replaces the lines 20–61 logic with a more generalized approach.
    """
    # 1. Validate input data
    if not data or "transcript" not in data:
        raise ValueError("Invalid transcript format. Missing 'transcript' key.")

    transcript_segments = data.get("transcript", [])
    transcript_text = " ".join(seg.get("transcript", "") for seg in transcript_segments).strip()
    
    if not transcript_text:
        raise ValueError("Transcript text is empty.")

    # 2. Choose which prompts/keys you want to process
    prompts_to_call = ["tldr", "measurableBuisnessImpacts", "followUpEmail"]

    # 3. Call the multi-request processor
    combined_results = process_ai_requests(
        client=client,
        prompt_keys=prompts_to_call,
        transcript_text=transcript_text
    )

    # 4. Print the results
    print("Combined AI Results:")
    pprint(combined_results, indent=4)
    # Each item in combined_results corresponds to {"promptKey": <>, "result": <>}

    return combined_results

@app.route('/transcript/ai-process', methods=['POST'])
def ai_process_transcript():
    try:
        data = request.get_json()
        print(data)
        output = main_logic(client, data)
        return jsonify(output), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def temp_process_test():
    with open("../docs/grain_transcript.json", "r") as f:
        data = json.load(f)

    output = main_logic(client, data)

    # Create an application context so that Flask's jsonify works properly.
    with app.app_context():
        result_json = jsonify(output)
        print("Anthropic Combined Results:")
        pprint(output)
        return result_json, 200

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        temp_process_test()
    else:
        app.run(debug=True) 