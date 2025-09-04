"""Books Service."""

from sqlalchemy.orm import Session

from app.database.operations import book_operations
from app.schemas import books as books_schemas


def get_books(
    db: Session,
) -> list[books_schemas.BookModel]:
    return book_operations.get_books(db=db)


def get_book_by_id(
    id: books_schemas.BookId,
    db: Session,
) -> books_schemas.BookModel:
    return book_operations.get_book_by_id(id=id, db=db)


def create_book(
    book_create_model: books_schemas.BookCreateModel,
    db: Session,
) -> books_schemas.BookModel:
    return book_operations.create_book(book_create_model=book_create_model, db=db)
