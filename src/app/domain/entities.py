from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from src.app.domain.enums import HairCutEnum
from src.app.domain.exceptions import (
    DateFieldException,
    EmailFieldException,
    EmptyFieldException,
    InvalidChoiceFieldException,
    MinLenghtFieldException,
)
from src.app.domain.genericValidations import IdFieldValidation, RequiredFieldValidation


class User:

    def __init__(self , name : str , email : str , password : str)->None:
        self.__id = None
        self.name = name
        self.email = email
        self.password = password

    @property
    def id(self)->int | None:
        return self.__id

    @id.setter
    def id(self , id : int)->None:
        self.__id = IdFieldValidation.validate("id",id)

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self , email : str)->None:
        validate_email = RequiredFieldValidation.validate("email" , email)

        if "@" not in validate_email:
            raise EmailFieldException()

        self.__email = validate_email

    @property
    def name(self)->str:
        return self.__name

    @name.setter
    def name(self,name : str)->None:
        self.__name = RequiredFieldValidation.validate("name" , name)

    @property
    def password(self) -> str :
        return self.__password

    @password.setter
    def password(self , password : str):
        validate_password = self.validate_password(password)
        self.__password = validate_password

    @staticmethod
    def validate_password(password:str) -> str:
        validate_password = RequiredFieldValidation.validate("password",password)

        if len(validate_password) < 8 :
            raise MinLenghtFieldException("'password' lenght can't be less then 8")

        return validate_password

    def __repr__(self):
        return f"{self.name}"

class Appointment:
    tzinfo=ZoneInfo("America/Sao_Paulo")

    def __init__(self , user_id : int , day_id : int , started_at : datetime , finish_at : datetime , type : HairCutEnum)->None:
        self.__id = None
        self.__user_id = user_id
        self.__day_id = day_id
        self.__started_at = started_at
        self.__finish_at = finish_at
        self.__type = type

    @property
    def id(self) -> int | None:
        return self.__id

    @id.setter
    def id(self , id : int)->None:
        self.__id = IdFieldValidation.validate("id",id)

    @property
    def user_id(self)-> int:
        return self.__user_id

    @user_id.setter
    def user_id(self,id : int) -> None:
        self.__user_id = IdFieldValidation.validate("user_id" , id)

    @property
    def day_id(self)-> int:
        return self.__day_id

    @day_id.setter
    def day_id(self , id : int) -> None:
        self.__day_id = IdFieldValidation.validate("day_id" , id)

    @property
    def started_at(self) -> datetime:
        return self.__started_at

    @started_at.setter
    def started_at(self , started_at : datetime) -> None:
        current_date = datetime.today().replace(tzinfo=self.tzinfo)

        if started_at.replace(tzinfo=self.tzinfo) < current_date:
            raise DateFieldException("The started date can't be less then now")

        self.__started_at = started_at

    @property
    def finish_at(self) -> datetime:
        return self.__finish_at #type: ignore[attr-defined]

    @finish_at.setter
    def finish_at(self , finish_at : datetime) -> None:
        current_date = datetime.today().replace(tzinfo=self.tzinfo)

        if finish_at.replace(tzinfo=self.tzinfo) < current_date:
            raise DateFieldException("The finish date can't be less then now")

        self.__finish_at = finish_at

    @property
    def type(self) -> HairCutEnum:
        return self.__type

    @type.setter
    def type(self , hair_cut_type : HairCutEnum) -> None:
        if hair_cut_type is None:
            raise EmptyFieldException("'hair cut type' is required")

        if hair_cut_type not in list(HairCutEnum):
            raise InvalidChoiceFieldException(f"{hair_cut_type} is not a valide choice")

        self.__type = hair_cut_type


    @classmethod
    def create(cls , user_id : int , day_id : int , started_at : datetime , finish_at : datetime , type : HairCutEnum)->"Appointment":
        instance = cls(user_id , day_id ,started_at, finish_at , type)
        instance.user_id = user_id
        instance.day_id = day_id
        instance.started_at = started_at
        instance.finish_at = finish_at
        instance.type = type
        return instance

class Day:
    def __init__(self , date : date , started_at : datetime , finish_at : datetime):
        self.date = date
        self.started_at = started_at
        self.finish_at = finish_at

    @property
    def id(self) -> int | None:
        return self.__id

    @id.setter
    def id(self , id : int)->None:
        self.__id = IdFieldValidation.validate("id",id)

    def count_available_schedules(self) -> int:
        """return how many schedules are available"""
        return int(self.finish_at.hour - self.started_at.hour)

    def get_schedule_time(self) -> timedelta :
        """return how long each schedule can be"""
        schedule_count = self.count_available_schedules()
        time = self.finish_at.hour - self.started_at.hour
        return timedelta(hours=time / schedule_count)

    def get_schedules(self):
        schedules_list = []
        time_started = self.started_at
        schedule_time = self.get_schedule_time()
        while time_started <= self.finish_at:
            started_time = time_started
            finish_time = started_time + schedule_time
            schedules_list.append((started_time , finish_time))

            time_started += schedule_time

        return schedules_list

    def get_free_schedules(self, appointments: list[Appointment]) -> list[tuple[datetime,datetime]]:
        schedules = self.get_schedules()
        return [ s for s in schedules if all(not (s[0] == a.started_at and s[1] == a.finish_at) for a in appointments) ]
