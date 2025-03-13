import requests
import time
import os
from dotenv import load_dotenv
from src.cost_tracker import CostTracker
import logging

# Load environment variables
load_dotenv()

# Configure logging
log_dir = os.path.join(os.path.dirname(__file__), '../logs')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'errors.log'),
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class LLMRouter:
    def __init__(self, providers):
        """Initialize router with a list of providers (already loaded from YAML)."""
        self.providers = sorted(providers, key=lambda p: p["cost_per_1k_tokens"])
        self.cost_tracker = CostTracker()

    def route_request(self, prompt):
        """Routes the request to the cheapest available LLM provider."""
        for provider in self.providers:
            start_time = time.time()
            api_key = os.getenv(provider["api_key"].strip("${}"))
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            data = {"inputs": prompt} if provider["name"] == "HuggingFace" else {"prompt": prompt, "max_tokens": 100}

            try:
                response = requests.post(provider["api_url"], json=data, headers=headers, timeout=provider["timeout"])
                response.raise_for_status()
                
                result = response.json()
                token_count = result.get("usage", {}).get("total_tokens", 100)  # Default 100 if missing
                cost = (token_count / 1000) * provider["cost_per_1k_tokens"]
                response_time = time.time() - start_time
                
                # Save log entry to CSV file
                self.cost_tracker.log_request(provider["name"], token_count, cost, response_time)

                return {
                    "modelUsed": provider["name"],
                    "cost": round(cost, 4),
                    "tokens": token_count,
                    "response": result.get("generated_text", result.get("text", ""))
                }
            except Exception as e:
                logging.error(f"Error with {provider['name']}: {str(e)}")
                print(f"Error with {provider['name']}: {str(e)}")

        return {"error": "All providers failed"}, 500
