from sqlalchemy import Column , Integer , String , Boolean , Float , ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Restaurant(Base):

    __tablename__ = "restaurants"
    id= Column(Integer , primary_key = True , index =True)
# one user can have many restaurant hai yo chai foreign key le bhanxa
    owner_id = Column(Integer ,ForeignKey("users.id"), nullable =False)
    name = Column(String(150), nullable = False)
    description= Column(String(500), nullable = True)
    address = Column(String(300), nullable = False)
    phone = Column(String(20), nullable = False)
    image = Column(String, nullable = True)
    is_active = Column(Boolean , default = False)
    is_approved = Column(Boolean , default = False) # Admin approves restaurants
    rating = Column(Float , default = 0.0)
    delivery_time = Column(Integer , default = 30)
    min_order = Column(Float , default =0.0)

    owner = relationship("User", backref = "restaurants")
    food_items = relationship("FoodItem", backref = "restaurant")