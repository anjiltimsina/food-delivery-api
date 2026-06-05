from pydantic import BaseModel , field_validator
from typing import List

class CartItemAdd(BaseModel):
    food_item_id : int
    quantity : int = 1

    @field_validator("quantity")
    def quantity_positive(cls ,v):
        if v<1 :
            raise ValueError("Quantity must beat least 1")
        return v
    
class CartItemResponse(BaseModel):
    id: int
    food_item_id: int
    quantity: int
    unit_price : float

    model_config = {"from_attributes": True}

class CartResponse(BaseModel):
    id : int
    user_id : int
    items : List[CartItemResponse] =[]
    total : float =0.0
    model_config ={"from_attributes": True}
