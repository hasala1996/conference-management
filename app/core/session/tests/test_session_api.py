from uuid import uuid4

import pytest
from adapters.database.models import (  # Asegúrate de importar el modelo Speaker
    ScheduledSession,
    Speaker,
)
from core.common.test_base import TestBase
from httpx import Response


class TestSessionAPI(TestBase):
    """
    Tests for Session API endpoints.
    """

    @pytest.fixture(autouse=True)
    def setup(self, admin_token: str):
        """
        Setup for each test.

        Args:
            admin_token (str): The admin token for authentication.
        """
        self.base_url = "api/v1/session"
        self.headers = {"Authorization": f"Bearer {admin_token}"}

    def get_seeded_session_id(self):
        """
        Helper method to get a seeded session ID from the database.
        """
        session = self.db_session.query(ScheduledSession).first()
        return session.id if session else None

    def get_available_speaker_id(self):
        """
        Helper method to get an available speaker ID from the database.
        """
        speaker = self.db_session.query(Speaker).first()
        return speaker.id if speaker else None

    def test_list_sessions(self):
        """
        Test retrieving a paginated list of sessions.
        """
        response: Response = self.client.get(
            f"{self.base_url}/", params={"page": 1, "limit": 10}, headers=self.headers
        )
        assert response.status_code == 200
        response_data = response.json()
        assert "items" in response_data
        assert "pagination" in response_data
        assert len(response_data["items"]) > 0
        for session in response_data["items"]:
            assert "id" in session
            assert "title" in session
            assert "is_active" in session

    def test_retrieve_session(self):
        """
        Test retrieving a specific session by ID.
        """
        session_id = self.get_seeded_session_id()
        response: Response = self.client.get(
            f"{self.base_url}/{session_id}", headers=self.headers
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == str(session_id)
        assert "title" in response_data
        assert "is_active" in response_data

    def test_create_session(self):
        """
        Test creating a new session.
        """
        speaker_id = self.get_available_speaker_id()
        assert speaker_id is not None, "No available speaker found in the database."

        payload = {
            "title": "New Session",
            "description": "A test session",
            "start_time": "2023-10-01T10:00:00",
            "end_time": "2023-10-01T12:00:00",
            "capacity": 100,
            "speakers": [str(speaker_id)],
        }
        response: Response = self.client.post(
            f"{self.base_url}/", json=payload, headers=self.headers
        )
        assert response.status_code == 201
        response_data = response.json()
        assert "id" in response_data
        assert response_data["title"] == payload["title"]
        assert response_data["description"] == payload["description"]
        assert response_data["start_time"] == payload["start_time"]
        assert response_data["end_time"] == payload["end_time"]
        assert response_data["capacity"] == payload["capacity"]

    def test_update_session(self):
        """
        Test updating an existing session.
        """
        session_id = self.get_seeded_session_id()
        payload = {
            "title": "Updated Session",
            "description": "Updated description",
            "capacity": 150,
        }
        response: Response = self.client.put(
            f"{self.base_url}/{session_id}", json=payload, headers=self.headers
        )
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["title"] == payload["title"]
        assert response_data["capacity"] == payload["capacity"]

    def test_delete_session(self):
        """
        Test deleting a session.
        """
        session_id = self.get_seeded_session_id()
        response: Response = self.client.delete(
            f"{self.base_url}/{session_id}", headers=self.headers
        )
        assert response.status_code == 204
        response: Response = self.client.get(
            f"{self.base_url}/{session_id}", headers=self.headers
        )
        deleted_session = (
            self.db_session.query(ScheduledSession).filter_by(id=session_id).first()
        )
        assert deleted_session.deleted_at is not None
