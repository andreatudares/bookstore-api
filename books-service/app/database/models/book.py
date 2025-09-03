"""Book Model."""

import datetime
import uuid

from sqlalchemy import UUID, Column, DateTime, Float, String

from app.database.models import base


class Book(base.Base):
    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    title = Column("title", String, nullable=False)
    author = Column("author", String, nullable=False)
    price = Column("price", Float, nullable=False)
    created_at = Column(
        "created_at",
        DateTime,
        nullable=False,
        default=datetime.datetime.now(datetime.UTC),
    )
    updated_at = Column(
        "updated_at",
        DateTime,
        nullable=False,
        default=datetime.datetime.now(datetime.UTC),
    )
    deleted_at = Column("deleted_at", DateTime)
