from pydantic import BaseModel , EmailStr

class SimpleResponse(BaseModel):
    detail : str

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
    email : EmailStr
    password : str

class UserProfile(
    BaseModel
):
    name : str
    email : str
