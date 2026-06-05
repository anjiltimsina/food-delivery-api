from pydantic import BaseModel , field_validator
from typing import Optional

class ReviewCreate(BaseModel):
    restaurant_id : int
    order_id : int
    rating : float 
    comment : Optional[str] =None

    @field_validator("rating")
    def rating_range(cls , v):
        if not 1.0 <= v <= 5.0 :
            raise ValueError("Rating must be between 1.0 & 5.0")
        return v

class ReviewResponse(BaseModel):
    id : int
    user_id : int
    restaurant_id : int
    order_id : int
    rating : float
    comment : Optional[str] = None
    
    model_config = {"from_attributes" : True}
    