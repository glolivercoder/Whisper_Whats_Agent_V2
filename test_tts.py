import requests
import json

# Test the chat API with TTS enabled
url = "http://localhost:8001/api/chat"
data = {
    "message": "Olá, este é um teste de TTS",
    "use_tts": True,
    "tts_engine": "gtts"
}

response = requests.post(url, json=data)
print("Status Code:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2, ensure_ascii=False))