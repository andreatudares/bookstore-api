"""Orders Router."""

from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas import orders as orders_schemas
from app.services import orders_service

router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(get_db)])


@router.get("/", status_code=status.HTTP_200_OK)
def get_orders(
    db: Session = Depends(get_db),
):
    return orders_service.get_orders(db=db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(
    order_create_model: orders_schemas.OrderCreateModel, db: Session = Depends(get_db)
):
    order_created = orders_service.create_order(
        order_create_model=order_create_model,
        db=db,
    )
    db.commit()
    return order_created
