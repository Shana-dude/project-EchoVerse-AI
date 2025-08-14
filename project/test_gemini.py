"""
Test script for Google Gemini API
"""

import requests
import json
from config import GOOGLE_GEMINI_API_KEY

def test_gemini_api():
    api_key = GOOGLE_GEMINI_API_KEY
    
    print(f"API Key length: {len(api_key) if api_key else 0}")
    print(f"API Key starts with: {api_key[:10] if api_key else 'None'}...")
    
    if not api_key:
        print("❌ No API key found")
        return
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": "Write a short paragraph about artificial intelligence."
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 1024,
        }
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        print("Making API request...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(json.dumps(result, indent=2))
        else:
            print("❌ Error!")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    test_gemini_api()
