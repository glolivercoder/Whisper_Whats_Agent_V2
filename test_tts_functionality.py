import requests
import json

# Test the chat API with TTS enabled
url = "http://localhost:8001/api/chat"
data = {
    "message": "Olá, este é um teste de TTS",
    "use_tts": True,
    "tts_engine": "gtts"
}

try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    result = response.json()
    print("Success:", result.get("success", False))
    print("Has Audio:", result.get("has_audio", False))
    if result.get("has_audio"):
        print("Audio Size:", result.get("audio_size", 0), "bytes")
        print("TTS Engine Used:", result.get("tts_info", {}).get("engine", "Unknown"))
        print("First 100 chars of audio data:", result.get("audio_data", "")[:100] + "...")
    else:
        print("No audio data returned")
except Exception as e:
    print("Error:", str(e))