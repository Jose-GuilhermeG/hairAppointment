from abc import ABC , abstractmethod

from src.app.domain.exceptions import ValidateException , EmptyFieldException

class IGenericValidation(ABC):

    @staticmethod
    @abstractmethod
    def validate(key : str , value : any ) -> any:
        pass

class RequiredFieldValidation(
    IGenericValidation
):

    @staticmethod
    def validate(key , value):
        if value is None:
                raise ValidateException(f"'{key}' can't be null")

        if not len(value):
            raise EmptyFieldException(f"'{key}' this field can't be empty")

        return value

class IdFieldValidation(
    IGenericValidation
):
    @staticmethod
    def validate(key , value):
        if not isinstance(value , int):
            raise ValidateException("The id field must be a integer")

        if value < 0 :
            raise ValidateException("The id field can't be negative")

        return value
