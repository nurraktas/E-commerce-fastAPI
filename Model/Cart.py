from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean
from database import Base
from sqlalchemy.orm import relationship


class Cart(Base):
    __tablename__ ="carts"

    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="cart")
    items= relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

   
class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id=Column(Integer, ForeignKey("carts.id"), nullable=False) #hangi sepete ait
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False) #hangi urune 
    quantity = Column(Integer, default=1)
    #bu parca kime ait
    cart = relationship("Cart" , back_populates="items")
    product= relationship("Product", back_populates="cart_items")