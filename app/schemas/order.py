from pydantic import BaseModel
from typing import List, Optional
from app.models.order import OrderStatus, PaymentStatus

class OrderItemResponse(BaseModel):
    id: int
    food_item_id: int
    quantity: int
    unit_price: float

    model_config = {"from_attributes": True}

class OrderCreate(BaseModel):
    delivery_address: str
    notes: Optional[str] = None

class OrderResponse(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    status: OrderStatus
    payment_status: PaymentStatus
    total_amount: float
    delivery_address: str
    notes: Optional[str] = None
    items: List[OrderItemResponse] = []

    model_config = {"from_attributes": True}

class OrderStatusUpdate(BaseModel):
    status: OrderStatus