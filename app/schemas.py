from pydantic import BaseModel, Field
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    username: str = Field(min_length=3, max_length=50)
    role: str

    class Config:
        from_attributes = True


class RoleUpdate(BaseModel):
    role: str


# -----------------
# Authentication
# -----------------

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)


class LoginResponse(BaseModel):
    token: str
    user: UserResponse
    expires_at: datetime

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
