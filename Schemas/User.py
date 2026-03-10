from pydantic import BaseModel, EmailStr
from typing import List, Optional


class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    username : str
    email: str
    is_staff: bool = False 

    class Config:
        from_attributes = True

# Register cevabı için
class RegisterResponse(BaseModel):
    success: bool
    message: str
    data: Optional[UserResponse] = None
