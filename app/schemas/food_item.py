from pydantic import BaseModel , field_validator
from typing import Optional

# “These are the only fields I will accept and validate for this request.”
class FoodItemCreate(BaseModel):
    name : str
    description : Optional[str] = None
    price : float
    category : Optional[str] = None

    @field_validator("price")
    def price_must_be_positive(cls, v):
        if v<=0:
            raise ValueError("Price must be greater than 0")
        return v
    

class FoodItemUpdate(BaseModel):
    name :Optional[str] = None
    description:Optional[str] = None
    price : Optional[str] = None
    category : Optional[str] = None
    is_available: Optional[bool] = None

class FoodItemResponse(BaseModel):
    id : int
    restaurant_id : int
    name : str
    description: Optional[str] = None
    price : float
    image : Optional[str] = None
    category: Optional[str] = None
    is_available : bool
    model_config = {"from_attributes" : True}


