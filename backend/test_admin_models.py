#!/usr/bin/env python
"""Test admin model management"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_admin_models():
    """Test admin model management"""
    
    print("=" * 60)
    print("ADMIN MODEL MANAGEMENT TESTING")
    print("=" * 60)
    
    # 1. Admin login
    print("\n[1/7] Testing Admin Login...")
    login_data = {
        "email": "admin@example.com",
        "password": "admin123456"
    }
    response = requests.post(f"{BASE_URL}/admin/login", json=login_data)
    assert response.status_code == 200, f"Admin login failed: {response.text}"
    token = response.json()["access_token"]
    print("✅ Admin login successful")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Create a model
    print("\n[2/7] Testing Create Model...")
    model_data = {
        "name": "test_model_1",
        "display_name": "Test Model 1",
        "description": "A test model",
        "model_path": "/path/to/model",
        "is_active": True,
        "is_default": False,
    }
    response = requests.post(f"{BASE_URL}/admin/models", json=model_data, headers=headers)
    assert response.status_code == 200, f"Create model failed: {response.text}"
    model = response.json()
    model_id = model["id"]
    print(f"✅ Model created: {model['name']} (ID: {model_id})")
    
    # 3. Get model detail
    print("\n[3/7] Testing Get Model Detail...")
    response = requests.get(f"{BASE_URL}/admin/models/{model_id}", headers=headers)
    assert response.status_code == 200, f"Get model detail failed: {response.text}"
    model = response.json()
    print(f"✅ Model detail retrieved: {model['name']}")
    
    # 4. List models
    print("\n[4/7] Testing List Models...")
    response = requests.get(f"{BASE_URL}/admin/models", headers=headers)
    assert response.status_code == 200, f"List models failed: {response.text}"
    models_data = response.json()
    print(f"✅ Models list retrieved: {models_data['total']} models")
    
    # 5. Update model
    print("\n[5/7] Testing Update Model...")
    update_data = {
        "display_name": "Updated Test Model 1",
        "description": "Updated description",
        "is_active": True,
    }
    response = requests.patch(f"{BASE_URL}/admin/models/{model_id}", json=update_data, headers=headers)
    assert response.status_code == 200, f"Update model failed: {response.text}"
    model = response.json()
    print(f"✅ Model updated: {model['display_name']}")
    
    # 6. Toggle model status
    print("\n[6/7] Testing Toggle Model Status...")
    response = requests.get(f"{BASE_URL}/admin/models/{model_id}/toggle", headers=headers)
    assert response.status_code == 200, f"Toggle model status failed: {response.text}"
    model = response.json()
    print(f"✅ Model status toggled: is_active={model['is_active']}")
    
    # 7. Delete model
    print("\n[7/7] Testing Delete Model...")
    response = requests.delete(f"{BASE_URL}/admin/models/{model_id}", headers=headers)
    assert response.status_code == 200, f"Delete model failed: {response.text}"
    print("✅ Model deleted successfully")
    
    print("\n" + "=" * 60)
    print("✅ ALL ADMIN MODEL MANAGEMENT TESTS PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_admin_models()
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

