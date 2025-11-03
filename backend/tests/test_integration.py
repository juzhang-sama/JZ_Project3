"""Integration tests for complete user workflows"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tempfile
import os


@pytest.fixture(scope="function")
def integration_db():
    """Create a test database for integration tests"""
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestingSessionLocal, engine
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    os.unlink(db_path)
    app.dependency_overrides.clear()


@pytest.fixture
def integration_client(integration_db):
    """Create a test client with integration database"""
    return TestClient(app)


class TestAuthenticationFlow:
    """Test complete authentication workflow"""

    def test_complete_auth_flow(self, integration_client):
        """Test register -> login -> get profile -> logout flow"""
        # Step 1: Register
        register_response = integration_client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password12345",
            },
        )
        assert register_response.status_code == 200
        user_data = register_response.json()
        assert user_data["username"] == "testuser"

        # Step 2: Login
        login_response = integration_client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "password12345"},
        )
        assert login_response.status_code == 200
        login_data = login_response.json()
        assert "access_token" in login_data
        token = login_data["access_token"]

        # Step 3: Get profile
        headers = {"Authorization": f"Bearer {token}"}
        profile_response = integration_client.get("/api/v1/auth/me", headers=headers)
        assert profile_response.status_code == 200
        profile_data = profile_response.json()
        assert profile_data["username"] == "testuser"
        assert profile_data["email"] == "test@example.com"

        # Step 4: Update profile
        update_response = integration_client.put(
            "/api/v1/auth/profile",
            json={"username": "newusername"},
            headers=headers,
        )
        assert update_response.status_code == 200
        updated_data = update_response.json()
        assert updated_data["username"] == "newusername"

        # Step 5: Logout
        logout_response = integration_client.post(
            "/api/v1/auth/logout",
            headers=headers,
        )
        assert logout_response.status_code == 200


class TestGenerationFlow:
    """Test complete generation workflow"""

    def test_complete_generation_flow(self, integration_client):
        """Test register -> login -> get models -> create task -> check status flow"""
        # Step 1: Register and login
        integration_client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password12345",
            },
        )
        login_response = integration_client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "password12345"},
        )
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Step 2: Get models
        models_response = integration_client.get("/api/v1/models")
        assert models_response.status_code == 200
        models = models_response.json()
        assert isinstance(models, list)

        # Step 3: Create generation task
        if models:
            model_name = models[0].get("name", "test_model")
            task_response = integration_client.post(
                "/api/v1/generation/create",
                json={
                    "prompt": "test prompt",
                    "model_name": model_name,
                },
                headers=headers,
            )
            assert task_response.status_code == 200
            task_data = task_response.json()
            assert "id" in task_data
            task_id = task_data["id"]

            # Step 4: Check task status
            status_response = integration_client.get(
                f"/api/v1/generation/status/{task_id}",
                headers=headers,
            )
            assert status_response.status_code == 200
            status_data = status_response.json()
            assert status_data["id"] == task_id

            # Step 5: Get task history
            history_response = integration_client.get(
                "/api/v1/generation/history",
                headers=headers,
            )
            assert history_response.status_code == 200
            history = history_response.json()
            assert isinstance(history, list)


class TestAdminFlow:
    """Test complete admin workflow"""

    def test_complete_admin_flow(self, integration_client, integration_db):
        """Test admin login -> manage users -> view statistics flow"""
        # Step 1: Create admin user
        from app.models.user import User
        from app.utils.password import hash_password

        TestingSessionLocal, engine = integration_db
        db = TestingSessionLocal()
        admin = User(
            username="admin_user",
            email="admin@example.com",
            password_hash=hash_password("admin123456"),
            is_active=True,
            is_admin=True,
            role="superadmin",
        )
        db.add(admin)
        db.commit()
        db.close()

        # Step 2: Admin login
        login_response = integration_client.post(
            "/api/v1/admin/login",
            json={"email": "admin@example.com", "password": "admin123456"},
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Step 3: Get admin profile
        profile_response = integration_client.get(
            "/api/v1/admin/me",
            headers=headers,
        )
        assert profile_response.status_code == 200
        profile_data = profile_response.json()
        assert profile_data["username"] == "admin_user"

        # Step 4: Get dashboard stats
        stats_response = integration_client.get(
            "/api/v1/admin/dashboard/stats",
            headers=headers,
        )
        assert stats_response.status_code == 200
        stats_data = stats_response.json()
        assert "total_users" in stats_data

        # Step 5: Get detailed statistics
        detailed_response = integration_client.get(
            "/api/v1/admin/statistics",
            headers=headers,
        )
        assert detailed_response.status_code == 200
        detailed_data = detailed_response.json()
        assert "total_users" in detailed_data
        assert "success_rate" in detailed_data

        # Step 6: List users
        users_response = integration_client.get(
            "/api/v1/admin/users",
            headers=headers,
        )
        assert users_response.status_code == 200
        users_data = users_response.json()
        assert "total" in users_data
        assert "users" in users_data


class TestErrorHandling:
    """Test error handling across workflows"""

    def test_unauthorized_access(self, integration_client):
        """Test unauthorized access to protected endpoints"""
        # Try to access protected endpoint without token
        response = integration_client.get("/api/v1/auth/me")
        assert response.status_code == 401

    def test_invalid_credentials(self, integration_client):
        """Test login with invalid credentials"""
        response = integration_client.post(
            "/api/v1/auth/login",
            json={"email": "nonexistent@example.com", "password": "wrongpassword"},
        )
        assert response.status_code == 401

    def test_duplicate_email_registration(self, integration_client):
        """Test registration with duplicate email"""
        # First registration
        integration_client.post(
            "/api/v1/auth/register",
            json={
                "username": "user1",
                "email": "test@example.com",
                "password": "password12345",
            },
        )
        
        # Second registration with same email
        response = integration_client.post(
            "/api/v1/auth/register",
            json={
                "username": "user2",
                "email": "test@example.com",
                "password": "password12345",
            },
        )
        assert response.status_code == 400

    def test_invalid_token(self, integration_client):
        """Test access with invalid token"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = integration_client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401

