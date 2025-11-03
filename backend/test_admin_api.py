#!/usr/bin/env python
"""Test admin API"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_admin_api():
    """Test admin API endpoints"""
    
    print("=" * 60)
    print("ADMIN API TESTING")
    print("=" * 60)
    
    # 1. Admin login
    print("\n[1/5] Testing Admin Login...")
    login_data = {
        "email": "admin@example.com",
        "password": "admin123456"
    }
    response = requests.post(f"{BASE_URL}/admin/login", json=login_data)
    if response.status_code != 200:
        print(f"❌ Admin login failed: {response.status_code}")
        print(response.text)
        return
    
    token = response.json()["access_token"]
    print(f"✅ Admin login successful")
    print(f"   Token: {token[:30]}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Get admin profile
    print("\n[2/5] Testing Get Admin Profile...")
    response = requests.get(f"{BASE_URL}/admin/me", headers=headers)
    if response.status_code != 200:
        print(f"❌ Get admin profile failed: {response.status_code}")
        print(response.text)
        return
    
    admin = response.json()
    print(f"✅ Admin profile retrieved")
    print(f"   Username: {admin['username']}")
    print(f"   Email: {admin['email']}")
    print(f"   Role: {admin['role']}")
    
    # 3. Get dashboard stats
    print("\n[3/5] Testing Get Dashboard Stats...")
    response = requests.get(f"{BASE_URL}/admin/dashboard/stats", headers=headers)
    if response.status_code != 200:
        print(f"❌ Get dashboard stats failed: {response.status_code}")
        print(response.text)
        return
    
    stats = response.json()
    print(f"✅ Dashboard stats retrieved")
    print(f"   Total Users: {stats['total_users']}")
    print(f"   Total Tasks: {stats['total_tasks']}")
    print(f"   Total Models: {stats['total_models']}")
    print(f"   Task Stats: {stats['task_stats']}")
    
    # 4. List users
    print("\n[4/5] Testing List Users...")
    response = requests.get(f"{BASE_URL}/admin/users", headers=headers)
    if response.status_code != 200:
        print(f"❌ List users failed: {response.status_code}")
        print(response.text)
        return
    
    users_data = response.json()
    print(f"✅ Users list retrieved")
    print(f"   Total: {users_data['total']}")
    print(f"   Users: {len(users_data['users'])}")
    for user in users_data['users']:
        print(f"     - {user['username']} ({user['email']})")
    
    # 5. Get user detail
    print("\n[5/5] Testing Get User Detail...")
    if users_data['users']:
        user_id = users_data['users'][0]['id']
        response = requests.get(f"{BASE_URL}/admin/users/{user_id}", headers=headers)
        if response.status_code != 200:
            print(f"❌ Get user detail failed: {response.status_code}")
            print(response.text)
            return
        
        user = response.json()
        print(f"✅ User detail retrieved")
        print(f"   ID: {user['id']}")
        print(f"   Username: {user['username']}")
        print(f"   Email: {user['email']}")
        print(f"   Is Admin: {user['is_admin']}")
        print(f"   Role: {user['role']}")
    
    print("\n" + "=" * 60)
    print("✅ ALL ADMIN API TESTS PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_admin_api()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

