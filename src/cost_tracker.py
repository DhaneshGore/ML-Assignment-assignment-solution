import csv
import os
from datetime import datetime

class CostTracker:
    def __init__(self, log_file="logs/requests.csv"):
        self.log_file = log_file
        self.ensure_csv_headers()

    def ensure_csv_headers(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["timestamp", "model_used", "tokens_used", "cost", "response_time"])

    def log_request(self, model, tokens, cost, duration):
        with open(self.log_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.get_current_timestamp(), model, tokens, f"${cost:.4f}", f"{duration:.2f}s"])

    @staticmethod
    def get_current_timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
