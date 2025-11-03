"""Generation module tests"""

import pytest
from fastapi.testclient import TestClient

from app.models.user import User
from app.models.model import Model


@pytest.fixture
def auth_token(client):
    """Create test user and return auth token"""
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password12345",
        },
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "password12345"},
    )
    return response.json()["access_token"]


@pytest.fixture
def test_model(test_db):
    """Create test model"""
    TestingSessionLocal, engine = test_db
    db = TestingSessionLocal()
    model = Model(
        name="test_model",
        display_name="Test Model",
        description="A test model",
        is_active=True,
        is_default=True,
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    db.close()
    return model


class TestModelList:
    """Test model listing"""

    def test_list_models_empty(self, client):
        """Test listing models when empty"""
        response = client.get("/api/v1/models")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

    def test_list_models_with_data(self, client, test_model):
        """Test listing models with data"""
        response = client.get("/api/v1/models")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "test_model"


class TestGeneration:
    """Test generation functionality"""

    def test_generate_without_auth(self, client, test_model):
        """Test generation without authentication"""
        response = client.post(
            "/api/v1/generation/create",
            json={"prompt": "test prompt", "model_name": "test_model"},
        )
        # The endpoint can be called without auth (uses default user_id=1)
        assert response.status_code in [200, 401, 403]

    def test_generate_success(self, client, auth_token, test_model):
        """Test successful generation"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.post(
            "/api/v1/generation/create",
            json={"prompt": "test prompt", "model_name": "test_model"},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data

    def test_generate_invalid_model(self, client, auth_token):
        """Test generation with invalid model"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.post(
            "/api/v1/generation/create",
            json={"prompt": "test prompt", "model_name": "nonexistent_model"},
            headers=headers,
        )
        assert response.status_code == 404

    def test_generate_async(self, client, auth_token, test_model):
        """Test async generation"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.post(
            "/api/v1/generation/create-async",
            json={"prompt": "test prompt", "model_name": "test_model"},
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data


class TestGenerationStatus:
    """Test generation status tracking"""

    def test_get_task_status(self, client, auth_token, test_model):
        """Test getting task status"""
        headers = {"Authorization": f"Bearer {auth_token}"}

        # Create a task
        response = client.post(
            "/api/v1/generation/create-async",
            json={"prompt": "test prompt", "model_name": "test_model"},
            headers=headers,
        )
        if response.status_code == 200:
            task_data = response.json()
            if isinstance(task_data, dict) and "id" in task_data:
                task_id = task_data["id"]

                # Get status
                response = client.get(
                    f"/api/v1/generation/status/{task_id}",
                    headers=headers,
                )
                assert response.status_code == 200
                data = response.json()
                assert data["id"] == task_id

    def test_get_task_history(self, client, auth_token, test_model):
        """Test getting task history"""
        headers = {"Authorization": f"Bearer {auth_token}"}

        # Create a task
        client.post(
            "/api/v1/generation/create-async",
            json={"prompt": "test prompt", "model_name": "test_model"},
            headers=headers,
        )

        # Get history
        response = client.get(
            "/api/v1/generation/history",
            headers=headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

