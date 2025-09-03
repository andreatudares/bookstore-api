"""Conftest."""

from collections.abc import Generator
from unittest.mock import MagicMock
import pytest

from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.main import app

pytest_plugins = [
    "fixtures.book",
]


@pytest.fixture()
def mock_db_session(mocker: MockerFixture) -> MagicMock:
    return mocker.MagicMock(spec=Session)


@pytest.fixture()
def test_client(
    mock_db_session: Session,
) -> Generator[TestClient, None, None]:
    def override_get_db():
        try:
            yield mock_db_session
        finally:
            ...

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.pop(get_db, None)
