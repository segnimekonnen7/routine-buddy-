#!/usr/bin/env python3
"""Test script for ML-powered features."""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8002"

def test_health():
    """Test health endpoint."""
    print("🔍 Testing Health Endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_habits_endpoint():
    """Test habits endpoint."""
    print("🎯 Testing Habits Endpoint...")
    response = requests.get(f"{BASE_URL}/habits")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        habits = response.json()
        print(f"Found {len(habits)} habits:")
        for habit in habits:
            print(f"  - {habit['title']} (ID: {habit['id']})")
    print()

def test_ml_insights_endpoints():
    """Test the new ML insights endpoints."""
    print("🧠 Testing ML-Powered Insights Features...")
    
    # Test success prediction endpoint
    print("📊 Testing Success Prediction...")
    try:
        response = requests.get(f"{BASE_URL}/insights/habits/demo-1/success-prediction")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success Prediction: {result.get('prediction', 'N/A')} ({result.get('probability', 0)}%)")
            print(f"   Recommendation: {result.get('recommendation', 'N/A')}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    print()
    
    # Test optimal reminder endpoint
    print("⏰ Testing Optimal Reminder Time...")
    try:
        response = requests.get(f"{BASE_URL}/insights/habits/demo-1/optimal-reminder")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if 'suggested_reminder_hour' in result:
                print(f"✅ Optimal Reminder: {result['suggested_reminder_hour']}:00")
                print(f"   Confidence: {result.get('confidence', 0)}%")
            else:
                print(f"ℹ️  {result.get('message', 'No data available')}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    print()
    
    # Test completion stats endpoint
    print("📈 Testing Completion Stats...")
    try:
        response = requests.get(f"{BASE_URL}/insights/habits/demo-1/completion-stats")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Completion Stats: {result.get('total_completions', 0)} completions")
            print(f"   Rate: {result.get('completion_rate', 0)} per day")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    print()

def test_habit_insights():
    """Test comprehensive habit insights."""
    print("🔍 Testing Comprehensive Habit Insights...")
    try:
        response = requests.get(f"{BASE_URL}/insights/habits/demo-1/insights")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Habit Insights for: {result.get('habit_title', 'N/A')}")
            print(f"   Trend: {result.get('trend', 'N/A')}")
            print(f"   Weekly Rate: {result.get('weekly_completion_rate', 0)}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    print()

def test_recommendations():
    """Test personalized recommendations."""
    print("💡 Testing Personalized Recommendations...")
    try:
        response = requests.get(f"{BASE_URL}/insights/habits/demo-1/recommendations")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Recommendations for: {result.get('habit_title', 'N/A')}")
            recommendations = result.get('recommendations', [])
            print(f"   Found {len(recommendations)} recommendations:")
            for rec in recommendations:
                print(f"     - {rec.get('title', 'N/A')}: {rec.get('message', 'N/A')}")
        else:
            print(f"❌ Error: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    print()

def main():
    """Run all tests."""
    print("🚀 Testing Habit Loop ML-Powered Features")
    print("=" * 60)
    print()
    
    test_health()
    test_habits_endpoint()
    test_ml_insights_endpoints()
    test_habit_insights()
    test_recommendations()
    
    print("✅ All tests completed!")
    print()
    print("🎉 ML Features Implemented:")
    print("   • Smart Reminder Service (pandas/numpy analysis)")
    print("   • Success Prediction Analytics (rule-based ML)")
    print("   • Completion Statistics (statistical analysis)")
    print("   • Comprehensive Habit Insights (trend analysis)")
    print("   • Personalized Recommendations (ML-driven)")
    print()
    print("📚 Check the API docs at: http://localhost:8002/docs")

if __name__ == "__main__":
    main()
