from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean
from database import Base
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"

    id=Column(Integer, primary_key=True, index=True)
    name= Column(String, index=True)
    description =Column(String)
    price = Column(Float)
    stock = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    category = relationship("Category", back_populates="products")
