"""Book Client."""

import requests

from app import exceptions as http_exceptions
from app.clients import schemas as client_schemas
from app.settings import book_service_setting


def get_book(
    book_id: client_schemas.BookId,
) -> client_schemas.BookMessageModel:
    try:
        response = requests.get(
            f"{book_service_setting.api_url}/books/{book_id}",
            timeout=book_service_setting.timeout,
        )
        if response.status_code == 404:
            raise http_exceptions.NotFoundException(
                detail=f"Book with id={book_id} not found."
            )
        response.raise_for_status()
        return client_schemas.BookMessageModel.model_validate(response.json())
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Failed to call Books API: {exc}") from exc
