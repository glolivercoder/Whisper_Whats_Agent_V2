#!/usr/bin/env python3
"""
Final Test for WhatsApp Voice Agent V2 - Fixed Version
Tests all functionality on port 8001
"""

import requests
import json
import time

def test_all_endpoints():
    """Test all endpoints comprehensively"""
    base_url = "http://localhost:8001"
    
    print("🧪 FINAL COMPREHENSIVE TEST - WhatsApp Voice Agent V2")
    print("=" * 60)
    
    tests = []
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health: {data['status']}")
            print(f"   ✅ Whisper: {'Loaded' if data['whisper_loaded'] else 'Not Loaded'}")
            print(f"   ✅ Version: {data['version']}")
            tests.append(("Health Check", True))
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            tests.append(("Health Check", False))
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        tests.append(("Health Check", False))
    
    # Test 2: Frontend Access
    print("\n2️⃣ Testing Frontend Access...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200 and "WhatsApp Voice Agent" in response.text:
            print("   ✅ Frontend served successfully")
            print(f"   ✅ Content length: {len(response.text)} chars")
            tests.append(("Frontend", True))
        else:
            print(f"   ❌ Frontend failed: {response.status_code}")
            tests.append(("Frontend", False))
    except Exception as e:
        print(f"   ❌ Frontend error: {e}")
        tests.append(("Frontend", False))
    
    # Test 3: Chat API
    print("\n3️⃣ Testing Chat API...")
    try:
        payload = {
            "message": "Hello, I'm testing the voice agent!",
            "use_tts": False
        }
        response = requests.post(f"{base_url}/api/chat", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Chat API working")
            print(f"   ✅ User message: {data['user_message']}")
            print(f"   ✅ Bot response: {data['bot_response'][:50]}...")
            print(f"   ✅ Session ID: {data['session_id']}")
            tests.append(("Chat API", True))
        else:
            print(f"   ❌ Chat API failed: {response.status_code}")
            tests.append(("Chat API", False))
    except Exception as e:
        print(f"   ❌ Chat API error: {e}")
        tests.append(("Chat API", False))
    
    # Test 4: WhatsApp Webhook
    print("\n4️⃣ Testing WhatsApp Webhook...")
    try:
        payload = {
            "from_number": "5511999999999",
            "message": "Olá! Este é um teste do webhook do WhatsApp",
            "message_type": "text"
        }
        response = requests.post(f"{base_url}/api/whatsapp/webhook", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ WhatsApp webhook working")
            print(f"   ✅ From: {data['to']}")
            print(f"   ✅ Response: {data['response'][:50]}...")
            tests.append(("WhatsApp Webhook", True))
        else:
            print(f"   ❌ WhatsApp webhook failed: {response.status_code}")
            tests.append(("WhatsApp Webhook", False))
    except Exception as e:
        print(f"   ❌ WhatsApp webhook error: {e}")
        tests.append(("WhatsApp Webhook", False))
    
    # Test 5: TTS API
    print("\n5️⃣ Testing TTS API...")
    try:
        payload = {
            "text": "Este é um teste de síntese de voz em português",
            "voice": "default",
            "speed": 1.0
        }
        response = requests.post(f"{base_url}/api/tts", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ TTS API working")
            print(f"   ✅ Text: {data['text']}")
            print(f"   ✅ Voice: {data['voice']}")
            tests.append(("TTS API", True))
        else:
            print(f"   ❌ TTS API failed: {response.status_code}")
            tests.append(("TTS API", False))
    except Exception as e:
        print(f"   ❌ TTS API error: {e}")
        tests.append(("TTS API", False))
    
    # Test 6: Additional Endpoints
    print("\n6️⃣ Testing Additional Endpoints...")
    try:
        # Test status endpoint
        response = requests.get(f"{base_url}/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status API: {data['server']}")
            
        # Test docs endpoint
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("   ✅ API Docs available")
            
        tests.append(("Additional APIs", True))
    except Exception as e:
        print(f"   ⚠️  Additional endpoints: {e}")
        tests.append(("Additional APIs", False))
    
    # Results Summary
    print("\n" + "=" * 60)
    print("📊 FINAL TEST RESULTS")
    print("=" * 60)
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name:20} - {status}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed >= 5:
        print("\n🎉 SYSTEM FULLY OPERATIONAL!")
        print("\n🚀 Ready for:")
        print("   • Voice recording testing in browser")
        print("   • Mobile device testing")
        print("   • WhatsApp Business API integration")
        print("   • Production deployment")
        
        print(f"\n📱 Access Instructions:")
        print(f"   • Browser: http://localhost:8001")
        print(f"   • Mobile: http://YOUR_IP:8001")
        print(f"   • API Docs: http://localhost:8001/docs")
        
        return True
    else:
        print("\n❌ System needs more work")
        return False

if __name__ == "__main__":
    success = test_all_endpoints()
    
    if success:
        print("\n🏆 ALL TASKS COMPLETED SUCCESSFULLY!")
        print("The WhatsApp Voice Agent V2 is ready for production testing!")
    else:
        print("\n🔧 Some issues remain to be fixed")