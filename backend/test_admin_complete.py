#!/usr/bin/env python
"""Complete admin API testing"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_admin_complete():
    """Test complete admin functionality"""
    
    print("=" * 60)
    print("COMPLETE ADMIN API TESTING")
    print("=" * 60)
    
    # 1. Admin login
    print("\n[1/8] Testing Admin Login...")
    login_data = {
        "email": "admin@example.com",
        "password": "admin123456"
    }
    response = requests.post(f"{BASE_URL}/admin/login", json=login_data)
    assert response.status_code == 200, f"Admin login failed: {response.text}"
    token = response.json()["access_token"]
    print("✅ Admin login successful")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Get admin profile
    print("\n[2/8] Testing Get Admin Profile...")
    response = requests.get(f"{BASE_URL}/admin/me", headers=headers)
    assert response.status_code == 200, f"Get admin profile failed: {response.text}"
    admin = response.json()
    print(f"✅ Admin profile: {admin['username']} ({admin['role']})")
    
    # 3. Get dashboard stats
    print("\n[3/8] Testing Get Dashboard Stats...")
    response = requests.get(f"{BASE_URL}/admin/dashboard/stats", headers=headers)
    assert response.status_code == 200, f"Get dashboard stats failed: {response.text}"
    stats = response.json()
    print(f"✅ Dashboard stats retrieved")
    print(f"   Users: {stats['total_users']}, Tasks: {stats['total_tasks']}, Models: {stats['total_models']}")
    
    # 4. List users
    print("\n[4/8] Testing List Users...")
    response = requests.get(f"{BASE_URL}/admin/users", headers=headers)
    assert response.status_code == 200, f"List users failed: {response.text}"
    users_data = response.json()
    print(f"✅ Users list retrieved: {users_data['total']} users")
    
    # 5. Get user detail
    print("\n[5/8] Testing Get User Detail...")
    if users_data['users']:
        user_id = users_data['users'][0]['id']
        response = requests.get(f"{BASE_URL}/admin/users/{user_id}", headers=headers)
        assert response.status_code == 200, f"Get user detail failed: {response.text}"
        user = response.json()
        print(f"✅ User detail retrieved: {user['username']}")
    
    # 6. List tasks
    print("\n[6/8] Testing List Tasks...")
    response = requests.get(f"{BASE_URL}/admin/tasks", headers=headers)
    assert response.status_code == 200, f"List tasks failed: {response.text}"
    tasks_data = response.json()
    print(f"✅ Tasks list retrieved: {tasks_data['total']} tasks")
    
    # 7. List models
    print("\n[7/8] Testing List Models...")
    response = requests.get(f"{BASE_URL}/admin/models", headers=headers)
    assert response.status_code == 200, f"List models failed: {response.text}"
    models_data = response.json()
    print(f"✅ Models list retrieved: {models_data['total']} models")
    
    # 8. Test permission denied for non-admin
    print("\n[8/8] Testing Permission Denied for Non-Admin...")
    # First create a regular user
    register_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    if response.status_code == 200:
        # Login as regular user
        login_data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            user_token = response.json()["access_token"]
            user_headers = {"Authorization": f"Bearer {user_token}"}
            
            # Try to access admin endpoint
            response = requests.get(f"{BASE_URL}/admin/me", headers=user_headers)
            assert response.status_code == 403, f"Expected 403, got {response.status_code}"
            print("✅ Permission denied for non-admin user")
    
    print("\n" + "=" * 60)
    print("✅ ALL ADMIN API TESTS PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_admin_complete()
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

