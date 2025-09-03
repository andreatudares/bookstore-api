"""Book Fixtures."""

import datetime
import uuid
import faker
import pytest

from typing import Any

from app.schemas import books as books_schemas

fake = faker.Faker()


def build_book_create_model(
    **kwargs: dict[str, Any],
) -> books_schemas.BookCreateModel:
    params = dict(
        title=fake.name(),
        author=fake.name(),
        price=round(
            float(fake.pydecimal(left_digits=2, right_digits=2, positive=True)), 2
        ),
    )
    params.update(kwargs)
    return books_schemas.BookCreateModel.model_validate(params)


@pytest.fixture()
def book_create_model() -> books_schemas.BookCreateModel:
    return build_book_create_model()


def build_book_model(
    **kwargs: dict[str, Any],
) -> books_schemas.BookModel:
    params = dict(
        id=books_schemas.BookId(uuid.uuid4()),
        title=fake.name(),
        author=fake.name(),
        price=round(
            float(fake.pydecimal(left_digits=2, right_digits=2, positive=True)), 2
        ),
        created_at=datetime.datetime.now(datetime.UTC),
        updated_at=datetime.datetime.now(datetime.UTC),
        deleted_at=None,
    )
    params.update(kwargs)
    return books_schemas.BookModel.model_validate(params)


@pytest.fixture()
def book_model() -> books_schemas.BookModel:
    return build_book_model()
