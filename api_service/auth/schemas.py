from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: str = Field(..., example="sumit@gmail.com")
    password: str = Field(..., example="sumit")
    fullname: str = Field(..., example="sumit kumar")
    phone_number: int = Field(..., example="8540021732")
    state: str = Field(..., example="sumit kumar")
    city: str = Field(..., example="sumit kumar")


class UserList(BaseModel):
    user_id: str = None
    email: str
    fullname: str
    phone_number: int
    state: str
    city: str
    created_on: Optional[datetime] = None
    status: str = None


class UserListStatus(UserList):
    status: str


class UserPWD(UserList):
    password: str


class PhoneRequest(BaseModel):
    phone_number: int


class ResetPassword(BaseModel):
    new_password: str
    confirm_password: str


class TokenData(BaseModel):
    phone_number: int = None


class ChangePassword(BaseModel):
    old_password: str = Field(..., example="old password")
    new_password: str = Field(..., example="new password")
    confirm_password: str = Field(..., example="confirm password")
