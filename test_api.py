#!/usr/bin/env python3
"""Test API connectivity."""

import requests
import json

def test_api():
    """Test the API endpoints."""
    base_url = "http://localhost:8001"
    
    print("🔍 Testing API connectivity...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test habits endpoint
    try:
        response = requests.get(f"{base_url}/habits")
        print(f"✅ Habits endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Found {len(data)} habits")
            for habit in data:
                print(f"   - {habit['title']} (streak: {habit['current_streak_length']})")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Habits endpoint failed: {e}")
    
    # Test CORS
    try:
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        response = requests.options(f"{base_url}/habits", headers=headers)
        print(f"✅ CORS preflight: {response.status_code}")
        print(f"   CORS headers: {dict(response.headers)}")
    except Exception as e:
        print(f"❌ CORS test failed: {e}")

if __name__ == "__main__":
    test_api()
