#!/usr/bin/env python3
import sqlite3
import os

# Test database connection and data
db_path = "agent_database.db"

if os.path.exists(db_path):
    print(f"✅ Database found: {db_path} (size: {os.path.getsize(db_path)} bytes)")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"📊 Tables: {[row[0] for row in tables]}")
        
        # Check conversation_logs count
        cursor.execute("SELECT COUNT(*) FROM conversation_logs")
        conv_count = cursor.fetchone()[0]
        print(f"💬 Conversation logs: {conv_count}")
        
        # Check unique sessions
        cursor.execute("SELECT COUNT(DISTINCT session_id) FROM conversation_logs")
        session_count = cursor.fetchone()[0]
        print(f"🔗 Unique sessions: {session_count}")
        
        # Sample recent conversations
        cursor.execute("""
            SELECT session_id, user_message, assistant_response, created_at 
            FROM conversation_logs 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        recent = cursor.fetchall()
        print(f"🔍 Recent conversations ({len(recent)}):")
        for i, (session, user, assistant, created) in enumerate(recent):
            print(f"  {i+1}. [{session[:8]}] User: '{user[:30]}...' | Bot: '{assistant[:30]}...' | {created}")
        
        conn.close()
        print("✅ Database test completed successfully")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
else:
    print(f"❌ Database not found: {db_path}")