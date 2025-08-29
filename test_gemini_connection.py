#!/usr/bin/env python3
"""
Test script for Google Gemini API connection
Run this to verify if the Gemini API key is working properly.
"""

import requests
import json
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_connection(api_key):
    """Test Gemini API connection with a simple request"""

    if api_key in ['', 'your-gemini-api-key-here', None]:
        print("❌ ERROR: GEMINI_API_KEY is not properly configured!")
        print("   Current value:", api_key)
        print("   Please set a valid Google Gemini API key in the .env file")
        return False

    print(f"🔗 Testing Gemini API connection...")
    print(f"   API Key: {api_key[:20]}***{api_key[-4:] if len(api_key) > 24 else api_key[-4:]}")

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

        payload = {
            "contents": [{
                "parts": [{"text": "Olá, você pode responder com uma mensagem simples de confirmação?"}]
            }],
            "generationConfig": {
                "maxOutputTokens": 50,
                "temperature": 0.7
            }
        }

        headers = {
            "Content-Type": "application/json"
        }

        print("📡 Sending test request to Gemini API...")
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        print(f"📊 Response Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()

            # Check if we got a valid response
            if 'candidates' in data and len(data['candidates']) > 0:
                response_text = data['candidates'][0].get('content', {}).get('parts', [{}])[0].get('text', '')
                print("✅ Gemini API is working!")
                print(f"   Response: {response_text[:100]}...")
                return True
            else:
                print("❌ Empty or invalid response from API")
                print(f"   Full response: {json.dumps(data, indent=2)}")
                return False

        elif response.status_code == 400:
            print("❌ Bad Request - Check API key format")
            try:
                error_data = response.json()
                print(f"   Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   Error response: {response.text}")

        elif response.status_code == 403:
            print("❌ Forbidden - API key might be invalid or disabled")
            try:
                error_data = response.json()
                print(f"   Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   Error response: {response.text}")

        elif response.status_code == 429:
            print("❌ Too Many Requests - Rate limit exceeded")
            try:
                error_data = response.json()
                print(f"   Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   Error response: {response.text}")

        else:
            print(f"❌ HTTP {response.status_code} - Unexpected error")
            try:
                error_data = response.json()
                print(f"   Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   Error response: {response.text}")

        return False

    except requests.exceptions.Timeout:
        print("❌ Connection timeout - Check network connectivity")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - Check internet connectivity")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def main():
    print("🤖 Gemini API Connection Test")
    print("=" * 50)

    # Get API key from environment
    api_key = os.getenv('GEMINI_API_KEY', '')

    # Test the connection
    success = test_gemini_connection(api_key)

    if success:
        print("\n🎉 SUCCESS! Gemini API is working properly.")
        print("   The system should now respond correctly to chat requests.")
        return 0
    else:
        print("\n💥 FAILURE! Gemini API is not working.")
        print("   Check the .env file and ensure GEMINI_API_KEY contains a valid API key.")
        print("\n📝 To get a Gemini API key:")
        print("   1. Go to https://makersuite.google.com/app/apikey")
        print("   2. Sign in with your Google account")
        print("   3. Create a new API key")
        print("   4. Copy the key and replace 'your-gemini-api-key-here' in .env")
        return 1

if __name__ == "__main__":
    sys.exit(main())