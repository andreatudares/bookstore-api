"""Orders Schemas."""

import datetime
import uuid
from typing import NewType

from pydantic import BaseModel, ConfigDict, field_validator

BookId = NewType("BookId", uuid.UUID)
OrderId = NewType("OrderId", uuid.UUID)
OrderItemId = NewType("OrderItemId", uuid.UUID)


class OrderItemModel(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: OrderItemId
    order_id: OrderId
    book_id: uuid.UUID
    quantity: int


class OrderModel(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: OrderId
    name: str
    phone_number: str | None = None
    total_amount: float
    order_items: list[OrderItemModel]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime | None


class OrderItemCreateModel(BaseModel):

    book_id: BookId
    quantity: int

    @field_validator("quantity")
    @classmethod
    def validate_quantity_greater_than_0(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be greater than 0.")
        return v


class OrderCreateModel(BaseModel):

    name: str
    phone_number: str | None = None
    order_items: list[OrderItemCreateModel]

    @field_validator("phone_number")
    @classmethod
    def validate_digits_are_numbers(cls, v):
        if v.isnumeric():
            return v
        raise ValueError("Phone number must have numbers only.")


class OrderUpdateModel(BaseModel):

    total_amount: float | None = None
    updated_at: datetime.datetime
