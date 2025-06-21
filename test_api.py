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

def test_create_task():
    """Test creating a task."""
    print("\nTesting create task endpoint...")
    try:
        payload = {
            "name": "Test Task",
            "description": "This is a test task",
            "user_id": 1,
            "priority": 2
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/tasks",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Created Task ID: {result['id']}")
            print(f"Task Name: {result['name']}")
            return result['id']  # Return task ID for other tests
        else:
            print(f"Response: {response.json()}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_list_tasks():
    """Test listing tasks."""
    print("\nTesting list tasks endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/tasks?user_id=1")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            tasks = response.json()
            print(f"Found {len(tasks)} tasks")
            for task in tasks:
                print(f"  - {task['name']} (ID: {task['id']}, Completed: {task['is_completed']})")
        else:
            print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_task(task_id):
    """Test getting a specific task."""
    print(f"\nTesting get task endpoint (ID: {task_id})...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/tasks/{task_id}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            task = response.json()
            print(f"Task: {task['name']} - {task['description']}")
            print(f"Priority: {task['priority']}, Completed: {task['is_completed']}")
        else:
            print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_complete_task(task_id):
    """Test completing a task."""
    print(f"\nTesting complete task endpoint (ID: {task_id})...")
    try:
        response = requests.put(f"{BASE_URL}/api/v1/tasks/{task_id}/complete")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            task = response.json()
            print(f"Task completed: {task['name']} - Completed: {task['is_completed']}")
        else:
            print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_update_task(task_id):
    """Test updating a task."""
    print(f"\nTesting update task endpoint (ID: {task_id})...")
    try:
        payload = {
            "name": "Updated Test Task",
            "description": "This task has been updated",
            "priority": 3
        }
        
        response = requests.put(
            f"{BASE_URL}/api/v1/tasks/{task_id}",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            task = response.json()
            print(f"Task updated: {task['name']} - Priority: {task['priority']}")
        else:
            print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_delete_task(task_id):
    """Test deleting a task."""
    print(f"\nTesting delete task endpoint (ID: {task_id})...")
    try:
        response = requests.delete(f"{BASE_URL}/api/v1/tasks/{task_id}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Task deleted: {result['message']}")
        else:
            print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_create_chat_history():
    """Test creating a chat history."""
    print("\nTesting create chat history endpoint...")
    try:
        payload = {
            "name": "Test Chat",
            "description": "This is a test chat history",
            "user_id": 1,
            "messages": json.dumps([
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"}
            ]),
            "model_used": "gpt-3.5-turbo",
            "tokens_used": 50
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/chat-history",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Created Chat History ID: {result['id']}")
            print(f"Chat Name: {result['name']}")
            return result['id']  # Return chat ID for other tests
        else:
            print(f"Response: {response.json()}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_list_chat_histories():
    """Test listing chat histories."""
    print("\nTesting list chat histories endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/chat-history?user_id=1")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            chat_histories = response.json()
            print(f"Found {len(chat_histories)} chat histories")
            for chat in chat_histories:
                print(f"  - {chat['name']} (ID: {chat['id']})")
        else:
            print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_chat_history(chat_id):
    """Test getting a specific chat history."""
    print(f"\nTesting get chat history endpoint (ID: {chat_id})...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/chat-history/{chat_id}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            chat = response.json()
            print(f"Chat: {chat['name']} - {chat['description']}")
            print(f"Model: {chat['model_used']}, Tokens: {chat['tokens_used']}")
        else:
            print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_update_chat_history_messages(chat_id):
    """Test updating chat history messages."""
    print(f"\nTesting update chat history messages endpoint (ID: {chat_id})...")
    try:
        updated_messages = json.dumps([
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "user", "content": "How are you?"},
            {"role": "assistant", "content": "I'm doing well, thank you for asking!"}
        ])
        
        payload = {
            "messages": updated_messages,
            "model_used": "gpt-4",
            "tokens_used": 120
        }
        
        response = requests.put(
            f"{BASE_URL}/api/v1/chat-history/{chat_id}/messages",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            chat = response.json()
            print(f"Chat messages updated: {chat['name']}")
            print(f"New model: {chat['model_used']}, New tokens: {chat['tokens_used']}")
            print(f"Messages length: {len(chat['messages'])} characters")
        else:
            print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_update_chat_history(chat_id):
    """Test updating chat history general fields."""
    print(f"\nTesting update chat history endpoint (ID: {chat_id})...")
    try:
        payload = {
            "name": "Updated Test Chat",
            "description": "This chat history has been updated"
        }
        
        response = requests.put(
            f"{BASE_URL}/api/v1/chat-history/{chat_id}",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            chat = response.json()
            print(f"Chat updated: {chat['name']} - {chat['description']}")
        else:
            print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_delete_chat_history(chat_id):
    """Test deleting a chat history."""
    print(f"\nTesting delete chat history endpoint (ID: {chat_id})...")
    try:
        response = requests.delete(f"{BASE_URL}/api/v1/chat-history/{chat_id}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Chat history deleted: {result['message']}")
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
    
    # Basic tests
    basic_tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("Process Answers", test_process_answers)
    ]
    
    results = []
    for test_name, test_func in basic_tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        results.append((test_name, success))
        time.sleep(1)
    
    # Task management tests
    print(f"\n{'='*20} Task Management Tests {'='*20}")
    
    # Create a task first
    task_id = test_create_task()
    if task_id:
        results.append(("Create Task", True))
        
        # Test getting the task
        success = test_get_task(task_id)
        results.append(("Get Task", success))
        time.sleep(1)
        
        # Test listing tasks
        success = test_list_tasks()
        results.append(("List Tasks", success))
        time.sleep(1)
        
        # Test updating the task
        success = test_update_task(task_id)
        results.append(("Update Task", success))
        time.sleep(1)
        
        # Test completing the task
        success = test_complete_task(task_id)
        results.append(("Complete Task", success))
        time.sleep(1)
        
        # Test deleting the task
        success = test_delete_task(task_id)
        results.append(("Delete Task", success))
    else:
        results.append(("Create Task", False))
    
    # Chat history tests
    print(f"\n{'='*20} Chat History Tests {'='*20}")
    
    # Create a chat history first
    chat_id = test_create_chat_history()
    if chat_id:
        results.append(("Create Chat History", True))
        
        # Test getting the chat history
        success = test_get_chat_history(chat_id)
        results.append(("Get Chat History", success))
        time.sleep(1)
        
        # Test listing chat histories
        success = test_list_chat_histories()
        results.append(("List Chat Histories", success))
        time.sleep(1)
        
        # Test updating chat history messages
        success = test_update_chat_history_messages(chat_id)
        results.append(("Update Chat Messages", success))
        time.sleep(1)
        
        # Test updating chat history general fields
        success = test_update_chat_history(chat_id)
        results.append(("Update Chat History", success))
        time.sleep(1)
        
        # Test deleting the chat history
        success = test_delete_chat_history(chat_id)
        results.append(("Delete Chat History", success))
    else:
        results.append(("Create Chat History", False))
    
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