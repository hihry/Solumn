import os
import sys
import requests
from dotenv import load_dotenv

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Load credentials from .env file
load_dotenv()

BASE_URL = os.getenv("OPENAI_BASE_URL", "https://k61neu9vlk.execute-api.us-east-1.amazonaws.com/prod/v1")
API_KEY = os.getenv("OPENAI_API_KEY")

def test_model_endpoint(prompt="Hi, who is ishowspeed ?"):
    if not API_KEY:
        print("[ERROR] OPENAI_API_KEY is not set in environment or .env file.")
        sys.exit(1)
        
    url = f"{BASE_URL.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-5.5",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    print(f"Connecting to OpenAI endpoint: {url}")
    print(f"Testing with model 'gpt-5.5'...")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print("\n[SUCCESS] API Key and Endpoint Verification Successful!")
            print(f"Model ID returned: {data.get('model', 'N/A')}")
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"\nResponse from model:\n{content}")
            return True
        else:
            print(f"\n[FAIL] API Call Failed with HTTP Status Code: {response.status_code}")
            print(f"Details: {response.text}")
            return False
    except Exception as e:
        print(f"\n[ERROR] Connection Error: {e}")
        return False

if __name__ == "__main__":
    test_model_endpoint()
