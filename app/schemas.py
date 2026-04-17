from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    name: str
    email: EmailStr
    age: int
    city: str
    is_active: bool
    role: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    city: str
    is_active: bool
    role: str

    class Config:
        from_attributes = True   # Pydantic understand SQLAlchemy objects through this when formatting a response

class UserUpdate(BaseModel): # This is  for patch - to update only some fields
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    city: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None