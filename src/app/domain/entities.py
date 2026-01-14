from src.app.domain.enums import HairCutEnum
from datetime import datetime , date

from src.app.domain.exceptions import EmailFieldException , MinLenghtFieldException , DateFieldException  , InvalidChoiceFieldException , EmptyFieldException
from src.app.domain.genericValidations import RequiredFieldValidation , IdFieldValidation

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
        validate_password = RequiredFieldValidation.validate("password",password)

        if len(validate_password) < 8 :
            raise MinLenghtFieldException("'password' lenght can't be less then 8")

        self.__password = validate_password

    def __repr__(self):
        return f"{self.name}"

class Appoinment:
    def __init__(self , user_id : int , started_at : date , finish_at : date , type : HairCutEnum)->None:
        self.__id = None
        self.user_id = user_id
        self.started_at = started_at
        self.finish_at = finish_at
        self.type = type

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
    def started_at(self) -> date:
        return self.__started_at

    @started_at.setter
    def started_at(self , started_at : date) -> None:
        current_date = date.today()

        if started_at < current_date:
            raise DateFieldException("The date can't be less then today")

        self.__started_at = started_at

    @property
    def finish_at(self) -> date:
        return self.__finish_at

    @finish_at.setter
    def finish_at(self , finish_at : date) -> None:
        current_date = date.today()

        if finish_at < current_date:
            raise DateFieldException("The date can't be less then today")

        self.__started_at = finish_at

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

    def get_schedule_time(self) -> float :
        """return how long each schedule can be"""
        schedule_count = self.count_available_schedules()
        time = self.finish_at.hour - self.started_at.hour
        return time / schedule_count
