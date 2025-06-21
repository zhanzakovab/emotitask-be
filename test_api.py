#!/usr/bin/env python3
"""
Simple test script to verify the API endpoints.
Run this after starting the server to test the endpoints.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_root():
    """Test the root endpoint."""
    print("\nTesting root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_models():
    """Test the models endpoint."""
    print("\nTesting models endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/models")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            models = response.json()
            print(f"Available models: {models[:5]}...")  # Show first 5 models
        else:
            print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_process_answers():
    """Test the process-answers endpoint."""
    print("\nTesting process-answers endpoint...")
    try:
        payload = {
            "user_id": 1,
            "question_answers": {
                "1": "I want to improve my productivity at work",
                "2": "I struggle with time management",
                "3": "I work in software development",
                "4": "I have about 2 hours of free time daily"
            },
            "model": "gpt-3.5-turbo",
            "max_tokens": 300,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/process-answers",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"User ID: {result['user_id']}")
            print(f"Generated Prompt: {result['prompt'][:200]}...")
            print(f"AI Response: {result['response'][:200]}...")
            print(f"Model: {result['model']}")
            if result.get('usage'):
                print(f"Usage: {result['usage']}")
        else:
            print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests."""
    print("Starting API tests...")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("Models Endpoint", test_models),
        ("Process Answers", test_process_answers)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        results.append((test_name, success))
        time.sleep(1)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print("TEST RESULTS:")
    print("=" * 50)
    
    all_passed = True
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not success:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the server logs for details.")
    print("=" * 50)

if __name__ == "__main__":
    main() 