# test_ai.py
import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, data):
    """Test an API endpoint"""
    try:
        response = requests.post(
            f"{BASE_URL}{endpoint}",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data)
        )
        print(f"\n=== Testing {endpoint} ===")
        print(f"Status: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        return response.json()
    except Exception as e:
        print(f"Error testing {endpoint}: {e}")
        return None

# Test documentation generation
test_endpoint("/api/docs/generate-function-doc", {
    "function_code": "def calculate_sum(a, b):\n    return a + b",
    "function_name": "calculate_sum"
})

# Test test generation
test_endpoint("/api/tests/generate-test", {
    "function_code": "def multiply_numbers(x, y):\n    return x * y",
    "function_name": "multiply_numbers"
})

# Test analysis
test_endpoint("/api/analysis/analyze-python", {
    "code": "def example():\n    print(\"hello\")\n\nclass Test:\n    def method(self):\n        pass"
})