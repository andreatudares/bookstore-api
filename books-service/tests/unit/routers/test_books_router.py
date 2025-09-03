"""Books Router Tests."""

import json
from unittest.mock import MagicMock

import pytest
from app.database import exceptions as db_exceptions
from app.schemas import books as books_schemas
from fastapi.testclient import TestClient
from fixtures import book as book_fixtures
from pytest_mock import MockerFixture


@pytest.fixture()
def mock_books_service(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("app.routers.books_router.books_service")


def test_get_books__ok(
    test_client: TestClient,
    mock_books_service: MagicMock,
):
    books_count = 2
    books_list = [book_fixtures.build_book_model() for i in range(books_count)]

    mock_books_service.get_books = MagicMock(return_value=books_list)

    response = test_client.get("/books/")

    expected_response = [json.loads(book.model_dump_json(by_alias=True)) for book in books_list]
    assert response.json() == expected_response
    assert response.status_code == 200

    mock_books_service.get_books.assert_called_once()


def test_get_books__empty_list(
    test_client: TestClient,
    mock_books_service: MagicMock,
):
    books_count = 0
    books_list = [book_fixtures.build_book_model() for i in range(books_count)]

    mock_books_service.get_books = MagicMock(return_value=books_list)

    response = test_client.get("/books/")

    assert response.json() == []
    assert response.status_code == 200

    mock_books_service.get_books.assert_called_once()


def test_get_book_by_id__ok(
    book_model: books_schemas.BookModel,
    test_client: TestClient,
    mock_books_service: MagicMock,
):
    mock_books_service.get_book_by_id = MagicMock(return_value=book_model)

    response = test_client.get(f"/books/{book_model.id}")

    assert response.status_code == 200
    assert response.json() == json.loads(book_model.model_dump_json(by_alias=True))

    mock_books_service.get_book_by_id.assert_called_once()


def test_get_book_by_id__not_found_exception(
    test_client: TestClient,
    mock_books_service: MagicMock,
):
    mock_books_service.get_book_by_id = MagicMock(
        side_effect=db_exceptions.DatabaseNotFoundException(message=""),
    )

    test_get_invalid_id = "00000000-0000-0000-0000-000000000000"

    response = test_client.get(f"/books/{test_get_invalid_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": ""}

    mock_books_service.get_book_by_id.assert_called_once()


def test_create_book__ok(
    book_create_model: books_schemas.BookCreateModel,
    book_model: books_schemas.BookModel,
    test_client: TestClient,
    mock_books_service: MagicMock,
):
    mock_books_service.create_book = MagicMock(return_value=book_model)

    response = test_client.post("/books/", json=book_create_model.model_dump(mode="json"))

    assert response.status_code == 201
    assert response.json() == json.loads(book_model.model_dump_json(by_alias=True))

    mock_books_service.create_book.assert_called_once()
