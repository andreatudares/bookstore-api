"""Order Operations."""

from pydantic import TypeAdapter
from sqlalchemy.orm import Session

from app.database import exceptions as db_exceptions
from app.database.models.order import Order, OrderItem
from app.schemas import orders as orders_schemas


def _get_order_by_id(
    id: orders_schemas.OrderId,
    db: Session,
) -> Order:
    order_from_db = (
        db.query(Order)
        .filter(
            Order.id == id,
        )
        .first()
    )

    if not order_from_db:
        raise db_exceptions.DatabaseNotFoundException(
            message=f"Order with id={id} not found."
        )

    return order_from_db


def get_orders(
    db: Session,
) -> list[orders_schemas.OrderModel]:
    return TypeAdapter(list[orders_schemas.OrderModel]).validate_python(
        db.query(Order).all()
    )


def create_order(
    order_create_model: orders_schemas.OrderCreateModel,
    total_amount: float,
    db: Session,
) -> orders_schemas.OrderModel:
    order_created = Order(
        name=order_create_model.name,
        phone_number=order_create_model.phone_number,
        total_amount=total_amount,
    )

    db.add(order_created)
    db.flush()

    return orders_schemas.OrderModel.model_validate(order_created)


def create_order_item(
    order_item_create_model: orders_schemas.OrderItemCreateModel,
    order_id: orders_schemas.OrderId,
    db: Session,
) -> orders_schemas.OrderItemModel:
    order_item_created = OrderItem(
        order_id=order_id,
        book_id=order_item_create_model.book_id,
        quantity=order_item_create_model.quantity,
    )

    db.add(order_item_created)
    db.flush()

    return orders_schemas.OrderItemModel.model_validate(order_item_created)


def update_order(
    order_id: orders_schemas.OrderId,
    order_update_model: orders_schemas.OrderUpdateModel,
    db: Session,
) -> orders_schemas.OrderModel:
    order_from_db = _get_order_by_id(
        id=order_id,
        db=db,
    )

    for attr, val in order_update_model.model_dump(exclude_unset=True).items():
        setattr(order_from_db, attr, val)

    db.add(order_from_db)

    return orders_schemas.OrderModel.model_validate(order_from_db)
