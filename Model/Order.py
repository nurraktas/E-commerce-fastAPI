from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean
from database import Base
from sqlalchemy.orm import relationship


class Order(Base):
    __tablename__ = "orders"
    id=Column(Integer,primary_key=True, index=True)
    user_id = Column (Integer, ForeignKey("users.id"))
   
    total_price = Column(Float)
    status = Column(String, default="Processing")

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__="order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Float)

    order = relationship("Order", back_populates="items")
    product= relationship("Product", back_populates="order_items")
