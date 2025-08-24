#!/usr/bin/env python3
"""
Server Verification Script
Checks which WhatsApp Voice Agent server is running and on which port.
"""

import requests
import json
from datetime import datetime

def check_server(port, server_name):
    """Check if server is running on specified port"""
    try:
        # Test health endpoint
        health_url = f"http://localhost:{port}/health"
        response = requests.get(health_url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {server_name}")
            print(f"   Port: {port}")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Version: {data.get('version', 'unknown')}")
            print(f"   Whisper Loaded: {data.get('whisper_loaded', False)}")
            if 'faster_whisper_loaded' in data:
                print(f"   Faster-Whisper: {data.get('faster_whisper_loaded', False)}")
            return True
        else:
            print(f"❌ {server_name} - HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {server_name} - Not running on port {port}")
        return False
    except requests.exceptions.Timeout:
        print(f"⚠️ {server_name} - Timeout on port {port}")
        return False
    except Exception as e:
        print(f"❌ {server_name} - Error: {e}")
        return False

def check_history_api(port):
    """Check if history API is available"""
    try:
        history_url = f"http://localhost:{port}/api/history/conversations"
        response = requests.get(history_url, timeout=5)
        
        if response.status_code == 200:
            print(f"   ✅ History API: Available")
            return True
        elif response.status_code == 404:
            print(f"   ❌ History API: Not Found (404)")
            return False
        else:
            print(f"   ⚠️ History API: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ History API: Error - {e}")
        return False

def main():
    print("🔍 WhatsApp Voice Agent Server Verification")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    servers_found = 0
    
    # Check Enhanced Server (port 8001)
    print("Checking Enhanced Server (main_enhanced.py):")
    if check_server(8001, "Enhanced Server"):
        servers_found += 1
        check_history_api(8001)
    print()
    
    # Check Simple Server (port 8002)  
    print("Checking Simple Server (simple_server.py):")
    if check_server(8002, "Simple Server"):
        servers_found += 1
        check_history_api(8002)
    print()
    
    # Check Fixed Server (port 8001 - alternative)
    print("Checking Fixed Server (main_fixed.py):")
    if check_server(8001, "Fixed Server"):
        # This would conflict with enhanced server on same port
        pass
    print()
    
    # Summary
    print("=" * 50)
    print("📊 SUMMARY:")
    
    if servers_found == 0:
        print("❌ No servers are currently running!")
        print("💡 Solution: Run 'START_ENHANCED_SERVER.bat' or 'python backend/main_enhanced.py'")
    elif servers_found == 1:
        # Check which one is running
        try:
            response = requests.get("http://localhost:8001/health", timeout=2)
            if response.status_code == 200:
                data = response.json()
                version = data.get('version', '')
                if 'enhanced' in version.lower():
                    print("✅ Enhanced Server is running correctly on port 8001")
                    print("✅ This is the CORRECT server for full functionality")
                else:
                    print("⚠️ A server is running on port 8001 but may not be the enhanced version")
        except:
            try:
                response = requests.get("http://localhost:8002/health", timeout=2)
                if response.status_code == 200:
                    print("⚠️ Simple Server is running on port 8002")
                    print("❌ This server has LIMITED functionality")
                    print("💡 Solution: Stop this server and run the Enhanced Server on port 8001")
            except:
                pass
    else:
        print("⚠️ Multiple servers are running - this may cause conflicts!")
        print("💡 Solution: Stop all servers and run only the Enhanced Server")
    
    print()
    print("🎯 RECOMMENDED ACTION:")
    print("1. Stop all running servers")
    print("2. Run: START_ENHANCED_SERVER.bat")
    print("3. Access: http://localhost:8001")
    print("4. Check Console Logs for confirmation")

if __name__ == "__main__":
    main()