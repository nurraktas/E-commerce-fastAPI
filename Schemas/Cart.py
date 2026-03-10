from pydantic import BaseModel, EmailStr
from typing import List, Optional


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemUpdate(BaseModel):
    quantity: int

# Sepetin içindeki ürün satırı
class CartItem(BaseModel):
    id: int
    product_id: int
    quantity: int
   
    class Config:
        from_attributes = True
        

class Cart(BaseModel):
    id: int
    user_id: int
    items: List[CartItem] = [] # Sepetin içindeki ürünler
    
    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    id: int
    user_id: int
    items: List[CartItem]

    class Config:
        from_attributes = True
