"""Orders Service."""

import datetime

from sqlalchemy.orm import Session

from app.clients import book as book_client
from app.database.operations import order_operations
from app.schemas import orders as orders_schemas


def get_orders(
    db: Session,
) -> list[orders_schemas.OrderModel]:
    return order_operations.get_orders(db=db)


def create_order(
    order_create_model: orders_schemas.OrderCreateModel,
    db: Session,
) -> orders_schemas.OrderModel:
    total_amount = 0.0

    order_created = order_operations.create_order(
        order_create_model=order_create_model,
        total_amount=total_amount,
        db=db,
    )

    for order_item in order_create_model.order_items:
        book_from_db = book_client.get_book(book_id=order_item.book_id)
        order_operations.create_order_item(
            order_item_create_model=orders_schemas.OrderItemCreateModel(
                book_id=order_item.book_id,
                quantity=order_item.quantity,
            ),
            order_id=order_created.id,
            db=db,
        )
        total_amount += order_item.quantity * book_from_db.price
    return order_operations.update_order(
        order_id=order_created.id,
        order_update_model=orders_schemas.OrderUpdateModel(
            total_amount=total_amount,
            updated_at=datetime.datetime.now(datetime.UTC),
        ),
        db=db,
    )
