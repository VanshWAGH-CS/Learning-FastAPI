from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from database import get_session
from models import Order, OrderCreate, OrderStatus, UpdateStatus

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=list[Order])
def get_orders(
    *,
    session: Session = Depends(get_session),
    status: Optional[OrderStatus] = Query(default=None),
):
    statement = select(Order)
    if status is not None:
        statement = statement.where(Order.status == status)
    return session.exec(statement).all()


@router.get("/{order_id}", response_model=Order)
def get_order(*, order_id: int, session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.post("", response_model=Order, status_code=status.HTTP_201_CREATED)
def create_order(*, order: OrderCreate, session: Session = Depends(get_session)):
    db_order = Order(
        customer_name=order.customer_name,
        customer_address=order.customer_address,
        customer_phone=order.customer_phone,
        status=OrderStatus.PREPARING,
    )
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order


@router.patch("/{order_id}/status", response_model=Order)
def update_order_status(
    *,
    order_id: int,
    updates: UpdateStatus,
    session: Session = Depends(get_session),
):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    order.status = updates.status
    order.updated_at = datetime.now(timezone.utc)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(*, order_id: int, session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    session.delete(order)
    session.commit()
    return None
