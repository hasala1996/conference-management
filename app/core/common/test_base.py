import pytest
from conftest import app
from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session


class TestBase:
    """
    Class to be inherited by all test classes.
    """

    @pytest.fixture(autouse=True)
    def initialize(self, db_session: Session) -> None:
        """
        Fixture that initializes the test environment.

        This fixture is used to set up the test environment before each test case is executed.
        It creates a TestClient object for making HTTP requests to the application and initializes the database session.

        Args:
            db_session (Session): The database session object.
        """
        self.client = TestClient(app)
        self.db_session: Session = db_session
