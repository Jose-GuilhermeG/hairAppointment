from sqlmodel import SQLModel , Field
from pydantic import EmailStr
from typing import Optional

class UserModel(SQLModel , table=True):
    id : Optional[int] = Field(primary_key=True , unique=True , default=None)
    name : str
    email : EmailStr = Field(unique=True)
    password : str
