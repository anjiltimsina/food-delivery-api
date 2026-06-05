from pydantic import BaseModel
from typing import Optional 

class RestaurantCreate(BaseModel):
    name: str
    description: Optional[str]= None
    address : str
    phone:str
    delivery_time : int = 30
    min_order : float = 0.0


class RestaurantUpdate(BaseModel):
    name :Optional[str] =None
    description:Optional[str] = None
    address :Optional[str] = None
    phone: Optional[str] = None
    delivery_time: Optional[int]  = None
    min_order : Optional[float] = None
    is_active :Optional[bool] =None

class RestaurantResponse(BaseModel):
    id : int
    owner_id : int
    description : Optional[str] =None
    address: str
    phone : str
    image:Optional[str] = None
    is_active : bool
    is_approved : bool
    rating: float

    model_config ={"from_attributes": True}
#You are allowed to create this schema from a Python object (like SQLAlchemy ORM model), not only from a dict.
#Pydantic expects: dictionary (JSON style)
#Pydantic can read Python objects (ORM models)