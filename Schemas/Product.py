from pydantic import BaseModel, EmailStr
from typing import List, Optional


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    
    class Config:
        from_attributes = True