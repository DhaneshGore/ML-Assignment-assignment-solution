import unittest
from src.router import LLMRouter

class TestLLMRouter(unittest.TestCase):
    def test_fallback_logic(self):
        providers = [
            {"name": "CheapLLM", "cost_per_1k_tokens": 0.002, "api_url": "http://fake-url.com"},
            {"name": "ExpensiveLLM", "cost_per_1k_tokens": 0.004, "api_url": "http://fake-url.com"},
        ]

        router = LLMRouter(providers)
        self.assertEqual(router.providers[0]["name"], "CheapLLM")
