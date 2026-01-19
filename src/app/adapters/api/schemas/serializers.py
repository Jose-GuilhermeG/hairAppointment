from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from src.app.domain.enums import HairCutEnum


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

class UpdateUser(
    BaseModel
):

    name : str | None

class AppointmentList(
    BaseModel
):
    started_at : datetime
    finish_at : datetime


class UserAppointmentList(
    AppointmentList
):
    type : HairCutEnum
    schedule : str

class AppointmentCreateIn(
    BaseModel
):
    started_at : datetime
    finish_at :  Optional[datetime] = None
    type : HairCutEnum
