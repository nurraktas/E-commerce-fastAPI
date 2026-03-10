from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True, index=True)
    username=Column(String, unique=True, index=True)
    email=Column(String, unique=True, index=True)
    hashed_password=Column(String)
    is_staff = Column(Boolean , default=False)

    cart = relationship("Cart", back_populates="user")
    orders = relationship("Order", back_populates="user")

