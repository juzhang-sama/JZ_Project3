#!/usr/bin/env python
"""Test admin task management and statistics"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_admin_tasks():
    """Test admin task management"""
    
    print("=" * 60)
    print("ADMIN TASK MANAGEMENT TESTING")
    print("=" * 60)
    
    # 1. Admin login
    print("\n[1/5] Testing Admin Login...")
    login_data = {
        "email": "admin@example.com",
        "password": "admin123456"
    }
    response = requests.post(f"{BASE_URL}/admin/login", json=login_data)
    assert response.status_code == 200, f"Admin login failed: {response.text}"
    token = response.json()["access_token"]
    print("✅ Admin login successful")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Get statistics
    print("\n[2/5] Testing Get Statistics...")
    response = requests.get(f"{BASE_URL}/admin/statistics", headers=headers)
    assert response.status_code == 200, f"Get statistics failed: {response.text}"
    stats = response.json()
    print("✅ Statistics retrieved")
    print(f"   Total Users: {stats['total_users']}")
    print(f"   Active Users: {stats['active_users']}")
    print(f"   Total Tasks: {stats['total_tasks']}")
    print(f"   Today Tasks: {stats['today_tasks']}")
    print(f"   Success Rate: {stats['success_rate']}%")
    print(f"   Task Stats: {stats['task_stats']}")
    
    # 3. List tasks
    print("\n[3/5] Testing List Tasks...")
    response = requests.get(f"{BASE_URL}/admin/tasks", headers=headers)
    assert response.status_code == 200, f"List tasks failed: {response.text}"
    tasks_data = response.json()
    print(f"✅ Tasks list retrieved: {tasks_data['total']} tasks")
    
    # 4. Get tasks by status
    print("\n[4/5] Testing Get Tasks by Status...")
    response = requests.get(f"{BASE_URL}/admin/tasks/status/completed", headers=headers)
    assert response.status_code == 200, f"Get tasks by status failed: {response.text}"
    status_tasks = response.json()
    print(f"✅ Completed tasks retrieved: {status_tasks['total']} tasks")
    
    # 5. List models
    print("\n[5/5] Testing List Models...")
    response = requests.get(f"{BASE_URL}/admin/models", headers=headers)
    assert response.status_code == 200, f"List models failed: {response.text}"
    models_data = response.json()
    print(f"✅ Models list retrieved: {models_data['total']} models")
    
    print("\n" + "=" * 60)
    print("✅ ALL ADMIN TASK MANAGEMENT TESTS PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_admin_tasks()
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

