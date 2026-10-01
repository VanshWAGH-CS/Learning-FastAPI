from sqlalchemy import func
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from database import get_session
from models import Order

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("")
def get_order_stats(*, session: Session = Depends(get_session)):
    total_orders = session.exec(select(func.count(Order.id))).one()
    status_counts = session.exec(
        select(Order.status, func.count(Order.id)).group_by(Order.status)
    ).all()

    by_status = {status.value: count for status, count in status_counts}
    return {"total_orders": total_orders, "by_status": by_status}
