"""Books Schemas."""

import datetime
import uuid
from typing import NewType

from pydantic import BaseModel, ConfigDict, field_validator

BookId = NewType("BookId", uuid.UUID)


class BookModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: BookId
    title: str
    author: str
    price: float
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime | None


class BookCreateModel(BaseModel):
    title: str
    author: str
    price: float

    @field_validator("price")
    @classmethod
    def validate_amount_greater_than_0(cls, v):
        if v <= 0:
            raise ValueError("Price must be greater than 0.")
        return round(v, 2)
