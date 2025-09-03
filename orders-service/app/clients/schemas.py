"""Book Client Schemas."""

import datetime
import uuid
from typing import NewType

from pydantic import BaseModel, ConfigDict

BookId = NewType("BookId", uuid.UUID)


class BookMessageModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: BookId
    title: str
    author: str
    price: float
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime | None
