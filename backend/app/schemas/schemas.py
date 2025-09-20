from pydantic import BaseModel,EmailStr
from datetime import datetime
from enum import Enum
from ..models.models import UserRole



# ================================
#   User schema
# ================================

class UserBase(BaseModel):
    name:str
    email:EmailStr
    role:UserRole=UserRole.customer
    
class UserCreate(UserBase):
    password:str
    
