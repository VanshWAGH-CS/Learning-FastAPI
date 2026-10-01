from enum import Enum
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field as SQLField
from sqlmodel import SQLModel

#order status (Enum) -> preparing, picked up, delivered, in transit, delivered

class OrderStatus(str, Enum):
    PREPARING = "preparing"
    PICKED_UP = "picked up"
    IN_TRANSIT = "in transit"
    DELIVERED = "delivered"

class Order(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)
    customer_name: str
    customer_address: str
    customer_phone: str
    status: OrderStatus = SQLField(default=OrderStatus.PREPARING)
    created_at: datetime = SQLField(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = SQLField(default_factory=lambda: datetime.now(timezone.utc))


#schema for order creation new order
class OrderCreate(BaseModel):
    customer_name: str
    customer_address: str
    customer_phone: str

#schema for updating the order status
class UpdateStatus(BaseModel):
    status: OrderStatus 


    