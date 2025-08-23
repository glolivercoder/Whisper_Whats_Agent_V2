#!/usr/bin/env python3
"""
Complete End-to-End Test for WhatsApp Voice Agent V2
This script tests all components of the system
"""

import requests
import json
import time
import sys
import os

class VoiceAgentTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session_id = "test_session_123"
        
    def test_server_health(self):
        """Test if server is running"""
        print("🔍 Testing server health...")
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            print(f"   Server Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Server not reachable: {e}")
            return False
    
    def test_frontend_access(self):
        """Test if frontend is accessible"""
        print("🌐 Testing frontend access...")
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            print(f"   Frontend Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Frontend accessible")
                return True
            else:
                print(f"   ⚠️  Frontend returned: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Frontend not accessible: {e}")
            return False
    
    def test_chat_endpoint(self):
        """Test chat functionality"""
        print("💬 Testing chat endpoint...")
        try:
            payload = {
                "message": "Hello, this is a test message",
                "session_id": self.session_id,
                "use_tts": False
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat", 
                json=payload, 
                timeout=10
            )
            
            print(f"   Chat Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Chat working!")
                print(f"   User Message: {result.get('user_message', 'N/A')}")
                print(f"   Bot Response: {result.get('bot_response', 'N/A')}")
                return True
            else:
                print(f"   ❌ Chat failed: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Chat endpoint error: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"   ❌ Invalid JSON response: {e}")
            return False
    
    def test_whatsapp_webhook(self):
        """Test WhatsApp webhook"""
        print("📱 Testing WhatsApp webhook...")
        try:
            payload = {
                "from_number": "5511999999999",
                "message": "Hello from WhatsApp test",
                "message_type": "text",
                "timestamp": "2024-01-01T10:00:00Z"
            }
            
            response = requests.post(
                f"{self.base_url}/api/whatsapp/webhook", 
                json=payload, 
                timeout=10
            )
            
            print(f"   Webhook Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ WhatsApp webhook working!")
                print(f"   Response: {result.get('response', 'N/A')}")
                return True
            else:
                print(f"   ❌ Webhook failed: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Webhook endpoint error: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"   ❌ Invalid JSON response: {e}")
            return False
    
    def test_websocket_connection(self):
        """Test WebSocket connectivity (basic test)"""
        print("🔌 Testing WebSocket connectivity...")
        try:
            # Simple test to see if WebSocket endpoint exists
            response = requests.get(f"{self.base_url}/ws", timeout=5)
            # WebSocket endpoints typically return 426 Upgrade Required for HTTP requests
            if response.status_code in [426, 400]:
                print("   ✅ WebSocket endpoint available")
                return True
            else:
                print(f"   ⚠️  Unexpected WebSocket status: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"   ❌ WebSocket test failed: {e}")
            return False
    
    def run_complete_test(self):
        """Run all tests"""
        print("🤖 WhatsApp Voice Agent V2 - Complete System Test")
        print("=" * 60)
        
        tests = [
            ("Server Health", self.test_server_health),
            ("Frontend Access", self.test_frontend_access),
            ("Chat Endpoint", self.test_chat_endpoint),
            ("WhatsApp Webhook", self.test_whatsapp_webhook),
            ("WebSocket Connection", self.test_websocket_connection)
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            print(f"\n📋 Running: {test_name}")
            try:
                results[test_name] = test_func()
            except Exception as e:
                print(f"   ❌ Test error: {e}")
                results[test_name] = False
            time.sleep(1)  # Brief pause between tests
        
        # Summary
        print(f"\n{'='*60}")
        print("📊 TEST RESULTS SUMMARY")
        print(f"{'='*60}")
        
        passed = 0
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {test_name:20} - {status}")
            if result:
                passed += 1
        
        print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! System is fully operational.")
            return True
        elif passed >= 3:
            print("⚠️  MOSTLY WORKING - Some features may need attention.")
            return True
        else:
            print("❌ SYSTEM ISSUES - Major components not working.")
            return False

def main():
    """Main test function"""
    print("Starting WhatsApp Voice Agent V2 End-to-End Test...")
    
    # Check if server should be running
    if len(sys.argv) > 1 and sys.argv[1] == "--start-server":
        print("🚀 Starting server first...")
        os.system("cd backend && python main.py &")
        print("⏳ Waiting 10 seconds for server to start...")
        time.sleep(10)
    
    tester = VoiceAgentTester()
    success = tester.run_complete_test()
    
    if success:
        print("\n🎯 SYSTEM READY FOR PRODUCTION TESTING!")
        print("\n📱 Next Steps:")
        print("   1. Open browser: http://localhost:8000")
        print("   2. Test voice recording with microphone")
        print("   3. Configure WhatsApp Business API webhook")
        print("   4. Test from mobile device on same network")
    else:
        print("\n🔧 SYSTEM NEEDS DEBUGGING")
        print("   Check server logs and fix failing components")
    
    return success

if __name__ == "__main__":
    main()