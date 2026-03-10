from pydantic import BaseModel, EmailStr
from typing import List, Optional


# A. Siparişin içinde görünecek
class ProductInOrder(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

    class Config:
        from_attributes = True

# B. Sipariş Satırı (Detay)
class OrderItem(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float # alindigi zaman satis fiyati 
   
    product: Optional[ProductInOrder] = None 

    class Config:
        from_attributes = True

# C. Sipariş Fişi 
class Order(BaseModel):
    id: int
    user_id: int
    status: str
    items: List[OrderItem] = [] # Sipariş detayları listesi
    
    class Config:
        from_attributes = True