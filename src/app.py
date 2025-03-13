from flask import Flask, request, jsonify
import yaml
import os
from src.router import LLMRouter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load provider configuration
with open("config/providers.yaml", "r") as file:
    config = yaml.safe_load(file)

app = Flask(__name__)
router = LLMRouter(config["providers"])

@app.route("/generate", methods=["POST"])
def generate_text():
    data = request.json
    prompt = data.get("prompt", "")

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    response_data = router.route_request(prompt)
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
