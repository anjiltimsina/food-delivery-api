from sqlalchemy import Column , Integer , String , Text , ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.base import Base

class Review(Base):

    __tablename__ = "reviews"

    id = Column(Integer , primary_key = True , index = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable = False)
    order_id = Column(Integer , ForeignKey("orders.id"), nullable = False)
    rating = Column(Float , nullable = False)
    comment = Column(Text , nullable = True)

    user = relationship("User", backref = "reviews")
    restaurant = relationship("Restaurant", backref = "reviews")