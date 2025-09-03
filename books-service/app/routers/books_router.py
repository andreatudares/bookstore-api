"""Books Router."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import exceptions as http_exceptions
from app.database import exceptions as db_exceptions
from app.database.session import get_db
from app.schemas import books as books_schemas
from app.services import books_service

router = APIRouter(prefix="/books", tags=["books"], dependencies=[Depends(get_db)])


@router.get("/", status_code=status.HTTP_200_OK)
def get_books(
    db: Session = Depends(get_db),
):
    return books_service.get_books(db=db)


@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_book_by_id(
    id: books_schemas.BookId,
    db: Session = Depends(get_db),
):
    try:
        return books_service.get_book_by_id(
            id=id,
            db=db,
        )
    except db_exceptions.DatabaseNotFoundException as err:
        raise http_exceptions.NotFoundException(detail=err.message)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_book(
    book_create_model: books_schemas.BookCreateModel, db: Session = Depends(get_db)
):
    book_created = books_service.create_book(
        book_create_model=book_create_model,
        db=db,
    )
    db.commit()
    return book_created
