"""Book Operations."""

from pydantic import TypeAdapter
from sqlalchemy.orm import Session

from app.database import exceptions as db_exceptions
from app.database.models.book import Book
from app.schemas import books as books_schemas


def _get_book_by_id(
    id: books_schemas.BookId,
    db: Session,
) -> Book:
    book_from_db = (
        db.query(Book)
        .filter(
            Book.id == id,
        )
        .first()
    )

    if not book_from_db:
        raise db_exceptions.DatabaseNotFoundException(
            message=f"Book with id={id} not found."
        )

    return book_from_db


def get_books(
    db: Session,
) -> list[books_schemas.BookModel]:
    return TypeAdapter(list[books_schemas.BookModel]).validate_python(
        db.query(Book).all()
    )


def get_book_by_id(
    id: books_schemas.BookId,
    db: Session,
) -> books_schemas.BookModel:
    return books_schemas.BookModel.model_validate(_get_book_by_id(id=id, db=db))


def create_book(
    book_create_model: books_schemas.BookCreateModel,
    db: Session,
) -> books_schemas.BookModel:
    book_created = Book(**book_create_model.model_dump(exclude_unset=True))
    print(book_created)
    db.add(book_created)
    db.flush()

    return books_schemas.BookModel.model_validate(book_created)
