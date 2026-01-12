from pydantic import BaseModel , EmailStr

class UserSessionCode(BaseModel):
    detail : str
    session_id : str


class UserRegisterIn(
    BaseModel
):
    name : str
    email : EmailStr
    password : str

class UserLoginIn(
    BaseModel
):
    email : str
    password : str

class UserProfile(
    BaseModel
):
    name : str
    email : str