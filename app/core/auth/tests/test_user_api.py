import pytest
from adapters.database.models.user_model import User
from core.common.test_base import TestBase
from httpx import Response


class TestUserAPI(TestBase):
    """
    Tests for User API endpoints.
    """

    @pytest.fixture(autouse=True)
    def setup(self, admin_token: str):
        """
        Setup for each test.

        Args:
            client (TestClient): The FastAPI test client.
            admin_token (str): The admin token for authentication.
        """
        self.base_url = "api/v1/user"
        self.headers = {"Authorization": f"Bearer {admin_token}"}

    def get_seeded_user_id(self):
        """
        Helper method to get a seeded user ID from the database.
        """
        user = self.db_session.query(User).first()
        return user.id if user else None

    def test_list_users(self):
        """
        Test retrieving a paginated list of users.
        """
        response: Response = self.client.get(
            f"{self.base_url}/", params={"page": 1, "limit": 10}, headers=self.headers
        )
        assert response.status_code == 200
        response_data = response.json()
        assert "items" in response_data
        assert "pagination" in response_data
        assert len(response_data["items"]) > 0
        for user in response_data["items"]:
            assert "id" in user
            assert "email" in user
            assert "is_active" in user

    def test_retrieve_user(self):
        """
        Test retrieving a specific user by ID.
        """
        user_id = self.get_seeded_user_id()
        response: Response = self.client.get(
            f"{self.base_url}/{user_id}", headers=self.headers
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == str(user_id)
        assert "email" in response_data
        assert "is_active" in response_data

    def test_create_user(self):
        """
        Test creating a new user.
        """
        payload = {
            "email": "testuser@example.com",
            "password": "securepassword123",
            "is_active": True,
        }
        response: Response = self.client.post(
            f"{self.base_url}/", json=payload, headers=self.headers
        )
        assert response.status_code == 201
        response_data = response.json()
        assert "id" in response_data
        assert response_data["email"] == payload["email"]
        assert response_data["is_active"] == payload["is_active"]

    def test_update_user(self):
        """
        Test updating an existing user.
        """
        user_id = self.get_seeded_user_id()
        payload = {
            "email": "updateduser@example.com",
            "password": "updatedpassword123",
            "is_active": False,
        }
        response: Response = self.client.put(
            f"{self.base_url}/{user_id}", json=payload, headers=self.headers
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["email"] == payload["email"]
        assert response_data["is_active"] == payload["is_active"]
        assert response_data["email"] == "updateduser@example.com"

    def test_delete_user(self):
        """
        Test deleting a user.
        """
        user_id = self.get_seeded_user_id()
        response: Response = self.client.delete(
            f"{self.base_url}/{user_id}", headers=self.headers
        )
        response_data = response.json()
        assert response.status_code == 200
        assert response_data["message"] == "User deleted successfully"
        response: Response = self.client.get(
            f"{self.base_url}/{user_id}", headers=self.headers
        )
        assert response.status_code == 404
