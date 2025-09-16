from pydantic import BaseModel
# In main.py or crud.py
from cloudinary_config import cloudinary
from typing import Optional, Literal


# ---------- User ----------
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional

class ReportBase(BaseModel):
    location: str
    landmark: Optional[str] = None
    size: Optional[str] = None
    content_type: str
    description: str

class ReportCreate(ReportBase):
    pass

class ReportResponse(ReportBase):
    id: int
    image_path: Optional[str]
    status: Optional[bool]

    class Config:
        orm_mode = True


class ReportResponse(BaseModel):
    id: int
    location: str
    landmark: Optional[str]
    size: Optional[str]
    content_type: str
    description: str
    image_path: str
    status: Optional[Literal["pending", "approved", "rejected"]] = "pending"

    class Config:
        from_attributes = True


class ReportBase(BaseModel):
    location: str
    landmark: Optional[str] = None
    size: Optional[str] = None
    content_type: str
    description: str

class ReportCreate(ReportBase):
    pass

class ReportResponse(BaseModel):
    id: int
    location: str
    landmark: Optional[str]
    size: Optional[str]
    content_type: str
    description: str
    image_path: str
    # ✅ Now only allows "pending", "approved", "rejected"
    status: Optional[Literal["pending", "approved", "rejected"]] = "pending"

    class Config:
        from_attributes = True
        
class ReportStatusResponse(BaseModel):
    id: int
    status: str

    class Config:
        orm_mode = True
        
        

class ReportCreate(BaseModel):
    location: str
    landmark: str | None = None
    size: str | None = None
    content_type: str
    description: str
    user_id: int | None = None  # make it optional
    
    
    
class ChangePassword(BaseModel):
    username: str
    new_password: str
    confirm_password: str