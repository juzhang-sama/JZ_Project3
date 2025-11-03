#!/usr/bin/env python
"""Test async generation API"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_async_generation():
    """Test async generation"""
    
    # Login
    print("1. Logging in...")
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code != 200:
        print(f"Login failed: {response.status_code}")
        print(response.text)
        return
    
    token = response.json()["access_token"]
    print(f"✅ Login successful, token: {token[:30]}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create async task
    print("\n2. Creating async generation task...")
    task_data = {
        "prompt": "a beautiful sunset over mountains",
        "model_name": "stable-diffusion-1.5"
    }
    response = requests.post(f"{BASE_URL}/generation/create-async", json=task_data, headers=headers)
    if response.status_code != 200:
        print(f"Task creation failed: {response.status_code}")
        print(response.text)
        return
    
    task = response.json()
    task_id = task["id"]
    print(f"✅ Async task created: {task_id}")
    print(f"   Status: {task['status']}")
    
    # Poll status
    print("\n3. Polling task status...")
    for i in range(30):
        time.sleep(1)
        response = requests.get(f"{BASE_URL}/generation/status/{task_id}", headers=headers)
        if response.status_code != 200:
            print(f"Status query failed: {response.status_code}")
            break
        
        status = response.json()["status"]
        print(f"   [{i+1}] Status: {status}")
        
        if status in ["completed", "failed"]:
            break
    
    # Get result
    print("\n4. Getting task result...")
    response = requests.get(f"{BASE_URL}/generation/result/{task_id}", headers=headers)
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Result retrieved")
        print(f"   Image URL: {result.get('image_url')}")
    else:
        print(f"Result retrieval failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_async_generation()

