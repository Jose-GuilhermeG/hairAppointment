from src.app.domain.enums import HairCutEnum
from dataclasses import dataclass
from datetime import date

from src.app.domain.exceptions import EmailFieldException , MinLenghtFieldException
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
@dataclass
class Appoinment:
    id : int | None
    user_id : int
    appoinment_date : date
    type : HairCutEnum
