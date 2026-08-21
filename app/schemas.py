from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    username: str


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    sender_id: int
    content: str


class MessageResponse(BaseModel):
    id: int
    sender_id: int
    sender: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True
