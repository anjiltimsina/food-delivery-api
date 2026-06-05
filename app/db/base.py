from sqlalchemy.orm import DeclarativeBase , declared_attr
from sqlalchemy import Column , DateTime , func


"""
class User(Base):

SQL table becomes:
users

"""
#yo chai declared_attr ko kamal ho hai
class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls) ->str:
        return cls.__name__.lower() +"s"
# This automatically creates table names.
    created_at = Column(DateTime(timezone =True), server_default = func.now())
    # when this row is craeted then created_at ma current time huncha
    updated_at = Column(DateTime(timezone = True), onupdate= func.now())
    #when this row is latest updated then updated_at ma current time huncha