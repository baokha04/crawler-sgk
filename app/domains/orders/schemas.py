from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class OrderBase(BaseModel):
    product_name: str
    quantity: int
    price: float

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    product_name: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None

class OrderInDBBase(OrderBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class Order(OrderInDBBase):
    pass
