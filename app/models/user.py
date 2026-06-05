import enum
from sqlalchemy import Column , Integer , String , Boolean , Enum
from app.db.base import Base

class UserRole(str , enum.Enum):
    ADMIN ='admin'
    CUSTOMER ="customer"
    RESTAURANT_OWNER = "restaurant_owner"
    DELIVERY_PERSON = "delivery_rider"
#An Enum restricts a field to a fixed set of values.

class User(Base):
#table name lekheni hunxa or nalekehe ni farak chai pardaina hai kinaki we have alreaddy named in the base.py with special function .
# kahile kahi custom name chaenxa tesko lagi ho , yo yeha lekhera override garna ta mili halxa ni
    __tablename__ = "users"
#An index makes searching faster.
    id = Column(Integer, primary_key = True , index = True)
    full_name = Column(String(100), nullable = False)
    email = Column(String(100), unique= True, index = True , nullable = False)
    phone = Column(String(20), unique=True, nullable=False)
    hashed_password = Column(String , nullable = False)
    role = Column(Enum(UserRole), default = UserRole.CUSTOMER , nullable = False)
    is_active = Column(Boolean , default = True)
    is_verified = Column(Boolean , default = False)
    profile_image = Column(String, nullable = True)

