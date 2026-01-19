from datetime import date as Date
from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlmodel import Field, Relationship, SQLModel

from src.app.domain.enums import HairCutEnum


class BaseEntitieModel(SQLModel):
    id : Optional[int] = Field(primary_key=True , unique=True , default=None)

class UserPermissionModel(BaseEntitieModel , table=True): #type: ignore[call-arg]
    user_id : int = Field(foreign_key="usermodel.id" )
    permission_id : int = Field(foreign_key="permissionmodel.id")

class UserModel(BaseEntitieModel , table=True): #type: ignore[call-arg]
    name : str
    email : EmailStr = Field(unique=True , index=True)
    password : str
    permissions : list["PermissionModel"] = Relationship(back_populates="users",link_model=UserPermissionModel)
    appointments : list["AppointmentModel"] = Relationship(back_populates="user")

class PermissionModel(BaseEntitieModel , table=True): #type: ignore[call-arg]
    name : str = Field(index=True , unique=True)
    users : list[UserModel] = Relationship(back_populates="permissions",link_model=UserPermissionModel)

class DayModel(BaseEntitieModel,table=True): #type: ignore[call-arg]
    date : Date
    started_at : datetime
    finish_at : datetime
    appointments : list["AppointmentModel"] = Relationship(back_populates="date")

class AppointmentModel(BaseEntitieModel , table = True): #type: ignore[call-arg]
    user_id : int | None = Field(default=None,foreign_key="usermodel.id")
    day_id : int | None = Field(default=None , foreign_key="daymodel.id")
    type : HairCutEnum
    started_at : datetime
    finish_at : datetime

    date : DayModel = Relationship(back_populates="appointments")
    user : UserModel = Relationship(back_populates="appointments")

    @hybrid_property
    def schedule(self)->str:
        return f"{self.started_at} - {self.finish_at}"

    @schedule.expression #type: ignore[no-redef]
    def schedule(cls):
        return func.concat(cls.started_at, " - ", cls.finish_at)

    model_config = { "ignored_types": (hybrid_property,) }
