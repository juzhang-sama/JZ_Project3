"""Authentication module tests"""

import pytest
from fastapi.testclient import TestClient

from app.models.user import User
from app.utils.password import hash_password


class TestUserRegistration:
    """Test user registration"""

    def test_register_success(self, client):
        """Test successful user registration"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password12345",  # At least 8 characters
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"

    def test_register_duplicate_email(self, client):
        """Test registration with duplicate email"""
        # First registration
        client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser1",
                "email": "test@example.com",
                "password": "password12345",
            },
        )
        # Second registration with same email
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser2",
                "email": "test@example.com",
                "password": "password12345",
            },
        )
        assert response.status_code == 400

    def test_register_invalid_email(self, client):
        """Test registration with invalid email"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser",
                "email": "invalid-email",
                "password": "password12345",
            },
        )
        assert response.status_code == 422

    def test_register_short_password(self, client):
        """Test registration with short password"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "short",
            },
        )
        assert response.status_code == 422


class TestUserLogin:
    """Test user login"""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        """Setup test user"""
        client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "password12345",
            },
        )

    def test_login_success(self, client):
        """Test successful login"""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "password12345"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        """Test login with wrong password"""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "wrongpassword"},
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user"""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "nonexistent@example.com", "password": "password12345"},
        )
        assert response.status_code == 401


class TestUserProfile:
    """Test user profile operations"""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        """Setup test user and get token"""
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
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def test_get_profile(self, client):
        """Test getting user profile"""
        response = client.get("/api/v1/auth/me", headers=self.headers)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"

    def test_update_profile(self, client):
        """Test updating user profile"""
        response = client.put(
            "/api/v1/auth/profile",
            json={"username": "newusername"},
            headers=self.headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newusername"

    def test_get_profile_without_token(self, client):
        """Test getting profile without token"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401

