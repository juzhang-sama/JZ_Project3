#!/usr/bin/env python
"""Complete Phase 3 testing"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_complete_flow():
    """Test complete generation flow"""
    
    print("=" * 60)
    print("PHASE 3 COMPLETE TESTING")
    print("=" * 60)
    
    # 1. Login
    print("\n[1/6] Testing Authentication...")
    login_data = {"email": "test@example.com", "password": "password123"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json()["access_token"]
    print("✅ Authentication successful")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Get models
    print("\n[2/6] Testing Model Listing...")
    response = requests.get(f"{BASE_URL}/models", headers=headers)
    assert response.status_code == 200, f"Model listing failed: {response.text}"
    models = response.json()
    print(f"✅ Found {len(models)} models")
    for model in models[:3]:
        print(f"   - {model['name']}: {model['display_name']}")
    
    # 3. Create sync task
    print("\n[3/6] Testing Synchronous Generation...")
    task_data = {
        "prompt": "a beautiful sunset",
        "model_name": models[0]["name"] if models else "stable-diffusion-1.5"
    }
    response = requests.post(f"{BASE_URL}/generation/create", json=task_data, headers=headers)
    assert response.status_code == 200, f"Sync task creation failed: {response.text}"
    sync_task = response.json()
    print(f"✅ Sync task created: {sync_task['id']}")
    print(f"   Status: {sync_task['status']}")
    
    # 4. Create async task
    print("\n[4/6] Testing Asynchronous Generation...")
    task_data = {
        "prompt": "a beautiful mountain landscape",
        "model_name": models[0]["name"] if models else "stable-diffusion-1.5"
    }
    response = requests.post(f"{BASE_URL}/generation/create-async", json=task_data, headers=headers)
    assert response.status_code == 200, f"Async task creation failed: {response.text}"
    async_task = response.json()
    async_task_id = async_task["id"]
    print(f"✅ Async task created: {async_task_id}")
    print(f"   Status: {async_task['status']}")
    
    # 5. Poll async task status
    print("\n[5/6] Testing Task Status Polling...")
    for i in range(5):
        time.sleep(1)
        response = requests.get(f"{BASE_URL}/generation/status/{async_task_id}", headers=headers)
        assert response.status_code == 200, f"Status query failed: {response.text}"
        status = response.json()["status"]
        print(f"   [{i+1}] Status: {status}")
        if status in ["completed", "failed"]:
            break
    
    # 6. Get task history
    print("\n[6/6] Testing Task History...")
    response = requests.get(f"{BASE_URL}/generation/history", headers=headers)
    assert response.status_code == 200, f"History query failed: {response.text}"
    history = response.json()
    print(f"✅ Retrieved {len(history)} tasks from history")
    for task in history[:3]:
        print(f"   - Task {task['id']}: {task['status']}")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nSummary:")
    print("- Authentication: ✅")
    print("- Model Listing: ✅")
    print("- Sync Generation: ✅")
    print("- Async Generation: ✅")
    print("- Status Polling: ✅")
    print("- Task History: ✅")

if __name__ == "__main__":
    try:
        test_complete_flow()
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

