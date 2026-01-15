from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserModel(SQLModel , table=True): #type: ignore[call-arg]
    id : Optional[int] = Field(primary_key=True , unique=True , default=None)
    name : str
    email : EmailStr = Field(unique=True , index=True)
    password : str
