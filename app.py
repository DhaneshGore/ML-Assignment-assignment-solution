from flask import Flask, request, jsonify
import yaml
import requests
import json
from time import time

app = Flask(__name__)

# Load configuration from providers.yaml
def load_providers_config():
    with open("providers.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config['providers']

# Make an actual API call to Hugging Face or other providers
def make_api_call(provider, prompt):
    headers = {
        "Authorization": f"Bearer {provider['api_key']}",
        "Content-Type": "application/json"
    }

    data = {
        "inputs": prompt
    }

    try:
        # Send the request to the respective model's endpoint
        response = requests.post(provider['endpoint'], headers=headers, json=data)

        # Log the response status code and content for debugging
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")

        # Check if the response is successful (status code 200)
        response.raise_for_status()

        if response.status_code == 200:
            result = response.json()

            # Extract generated text (may vary depending on the model)
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', 'No response')
            else:
                generated_text = 'No response'

            tokens_used = len(prompt.split())  # Approximate token count
            cost = (tokens_used / 1000) * provider.get('cost_per_1k_tokens', 0.01)

            return {
                'tokens': tokens_used,
                'cost': cost,
                'response': generated_text
            }

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

    return {"error": f"Failed to fetch response from {provider['name']}"}

# Generate endpoint to handle general prompts
@app.route('/generate', methods=['POST'])
def generate():
    # Get the user-provided prompt from the request body
    data = request.get_json()
    prompt = data['prompt']

    # Load providers from configuration file
    providers = load_providers_config()

    # Try each provider in order of priority
    for provider in sorted(providers, key=lambda x: x['priority']):
        result = make_api_call(provider, prompt)

        # If a provider returns a valid response, log it and return it
        if 'error' not in result:
            log_request(provider['name'], prompt, result)
            return jsonify({
                "modelUsed": provider['name'],
                "cost": result['cost'],
                "tokens": result['tokens'],
                "response": result['response']
            })
    
    # If all providers fail, return an error message
    return jsonify({"error": "All providers failed"})

# Log request data to a file (for debugging and record-keeping)
def log_request(provider_name, prompt, result):
    log_entry = {
        "timestamp": time(),
        "modelUsed": provider_name,
        "tokens": result["tokens"],
        "cost": result["cost"],
        "response": result["response"],
        "status": "success" if result["response"] else "failure"
    }
    with open("request_logs.json", "a") as log_file:
        json.dump(log_entry, log_file)
        log_file.write("\\n")  # Add a newline after each log entry

# Start the Flask app if this file is executed directly
if __name__ == "__main__":
    app.run(debug=True)
