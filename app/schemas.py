from pydantic import BaseModel, Field
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)


class UserResponse(BaseModel):
    id: int
    username: str = Field(min_length=3, max_length=50)

    class Config:
        from_attributes = True
#-----------------
# Message Schemas
#-----------------

class MessageCreate(BaseModel):
    client_id: str = Field(min_length=1, max_length=100)
    sender_id: int
    content: str = Field(min_length=1, max_length=2000)


class MessageResponse(BaseModel):
    id: int
    client_id: str = Field(min_length=1, max_length=100)
    sender_id: int
    sender: str
    content: str = Field(min_length=1, max_length=2000)
    timestamp: datetime

    class Config:
        from_attributes = True
