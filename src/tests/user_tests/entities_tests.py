import pytest

from src.app.domain.entities import User
from src.app.domain.exceptions import (
    EmailFieldException,
    EmptyFieldException,
    MinLenghtFieldException,
    ValidateException,
)


class UserValidationTest:
    """USer validation tests"""
    def test_if_id_can_be_a_string(self , simple_user : User):
        with pytest.raises(ValidateException):
            simple_user.id = "1"

    def test_if_id_can_be_odd(self , simple_user : User):
        with pytest.raises(ValidateException):
            simple_user.id = -1

    def test_if_id_can_be_none(self , simple_user : User):
        with pytest.raises(ValidateException):
            simple_user.id = None

    def test_if_name_can_be_empty(self):
        with pytest.raises(EmptyFieldException):
            user = User("","teste@email.com","teste") #noqa

    def test_if_email_can_be_empty(self):
        with pytest.raises(EmptyFieldException):
            user = User("teste user","","teste") #noqa

    def test_if_email_field_can_be_an_invalid_email(self):
        with pytest.raises(EmailFieldException):
            user = User("teste user","radonEmail","teste") #noqa

    def test_if_password_can_be_empty(self):
        with pytest.raises(EmptyFieldException):
            user = User("teste user","teste@email.com","") #noqa

    def test_if_password_lenght_can_be_less_then_eight(self):
        with pytest.raises(MinLenghtFieldException):
            user = User("teste user","teste@email.com","teste") #noqa

class UserMethodsTest:

    def test_eq_user_method(self , simple_user_data : dict):
        user_1 = User(**simple_user_data)
        user_2 = User(**simple_user_data)
        assert user_1 == user_2

    def test_repr_method(self , simple_user_data : dict):
        user = User(**simple_user_data)
        assert str(user) == simple_user_data["name"]
