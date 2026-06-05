import enum 
from sqlalchemy import Column, Integer, String , String , Float , ForeignKey , Enum , Text
from sqlalchemy.orm import relationship
from app.db.base import Base

class OrderStatus(str , enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    OUT_FOR_DELIVERY ="out_for_delivery"
    DELIVERD = "delivered"
    CANCELLED = "cancelled"

class PaymentStatus(str , enum.Enum):
    UNPAID ="unpaid"
    PAID ="paid"
    REFUNDED = "refunded"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer , primary_key = True , index =True)
    user_id = Column(Integer , ForeignKey("users.id"), nullable = False)
    restaurant_id = Column(Integer , ForeignKey("restaurants.id"), nullable = False)
    status = Column(Enum(OrderStatus), default = OrderStatus.PENDING)
    payment_status = Column(Enum(PaymentStatus), default = PaymentStatus.UNPAID)
    total_amount = Column(Float , nullable = False)
    delivery_address = Column(String(300), nullable = False)
    notes = Column(Text , nullable = True)

    user = relationship("User", backref = "orders")
    restaurant = relationship("Restaurant", backref = "orders")
    items = relationship("OrderItem", backref = "order", cascade ="all , delete-orphan")

# yo order chai Order class ko object ho hai

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    food_item_id = Column(Integer, ForeignKey("food_items.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)  # snapshot price at order time

    food_item = relationship("FoodItem")
    