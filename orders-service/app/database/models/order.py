"""Order Model."""

import datetime
import uuid

from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.database.models import base


class Order(base.Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = Column("name", String, nullable=False)
    phone_number = Column("phone_number", String, unique=True)
    total_amount = Column("total_amount", Float, nullable=False)
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

    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(base.Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    book_id = Column("book_id", UUID(as_uuid=True), nullable=False)
    quantity = Column("quantity", Integer, nullable=False)

    order = relationship("Order", back_populates="order_items")
