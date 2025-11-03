"""Admin module tests"""

import pytest
from fastapi.testclient import TestClient

from app.models.user import User
from app.utils.password import hash_password


@pytest.fixture
def admin_token(client, test_db):
    """Create admin user and return token"""
    TestingSessionLocal, engine = test_db
    db = TestingSessionLocal()
    admin = User(
        username="admin",
        email="admin@example.com",
        password_hash=hash_password("admin123456"),
        is_active=True,
        is_admin=True,
        role="superadmin",
    )
    db.add(admin)
    db.commit()
    db.close()

    response = client.post(
        "/api/v1/admin/login",
        json={"email": "admin@example.com", "password": "admin123456"},
    )
    return response.json()["access_token"]


@pytest.fixture
def user_token(client):
    """Create regular user and return token"""
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


class TestAdminAuth:
    """Test admin authentication"""

    def test_admin_login_success(self, admin_token):
        """Test successful admin login"""
        assert admin_token is not None

    def test_admin_login_wrong_password(self, client, test_db):
        """Test admin login with wrong password"""
        # Create admin first
        TestingSessionLocal, engine = test_db
        db = TestingSessionLocal()
        admin = User(
            username="admin",
            email="admin@example.com",
            password_hash=hash_password("admin123456"),
            is_active=True,
            is_admin=True,
            role="superadmin",
        )
        db.add(admin)
        db.commit()
        db.close()

        response = client.post(
            "/api/v1/admin/login",
            json={"email": "admin@example.com", "password": "wrongpassword"},
        )
        assert response.status_code == 401


class TestAdminAccess:
    """Test admin access control"""

    def test_admin_access_denied_for_user(self, client, user_token):
        """Test that regular users cannot access admin endpoints"""
        headers = {"Authorization": f"Bearer {user_token}"}
        response = client.get("/api/v1/admin/me", headers=headers)
        assert response.status_code == 403

    def test_admin_access_allowed(self, client, admin_token):
        """Test that admins can access admin endpoints"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get("/api/v1/admin/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "admin"
        assert data["role"] == "superadmin"


class TestAdminUserManagement:
    """Test admin user management"""

    def test_list_users(self, client, admin_token):
        """Test listing users"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get("/api/v1/admin/users", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "users" in data

    def test_get_user_detail(self, client, admin_token):
        """Test getting user detail"""
        # Create a user first
        client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password12345",
            },
        )

        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get("/api/v1/admin/users/2", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"

    def test_delete_user(self, client, admin_token):
        """Test deleting user"""
        # Create a user first
        client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password12345",
            },
        )

        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.delete("/api/v1/admin/users/2", headers=headers)
        assert response.status_code == 200


class TestAdminDashboard:
    """Test admin dashboard"""

    def test_dashboard_stats(self, client, admin_token):
        """Test getting dashboard stats"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get("/api/v1/admin/dashboard/stats", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_users" in data
        assert "total_tasks" in data
        assert "total_models" in data
        assert "task_stats" in data

    def test_statistics(self, client, admin_token):
        """Test getting detailed statistics"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get("/api/v1/admin/statistics", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert "total_users" in data
        assert "active_users" in data
        assert "success_rate" in data

