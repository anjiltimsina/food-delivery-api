from sqlalchemy import Column , Integer , String , ForeignKey, Float
from sqlalchemy.orm import relationship 
from app.db.base import Base

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key = True , index = True)
    user_id = Column(Integer , ForeignKey("users.id"),nullable = False)

    user = relationship("User" , backref= "cart")
    items = relationship("CartItem", backref ="cart", cascade="all, delete-orphan")

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer , primary_key = True , index = True)
    cart_id = Column(Integer , ForeignKey("carts.id"), nullable = False)
    food_item_id = Column(Integer, ForeignKey("food_items.id"), nullable = False)
    quantity = Column(Integer , default = 1 , nullable = False)
    unit_price = Column(Float , nullable = False)

    food_item = relationship("FoodItem", backref = "cart_items")

