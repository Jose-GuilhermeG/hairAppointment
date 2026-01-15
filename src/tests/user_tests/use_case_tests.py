import pytest

from src.app.application.use_cases import userUseCases
from src.app.domain.exceptions import ValidateException , IntegrityException
from src.app.application.ports.repository import IUserRepository
from src.app.domain.entities import User
from src.app.adapters.hashEncrypt import BcryptHashEncrypt

class TestRegisterUserCase:

    def test_if_register_is_create_a_user(self,user_repository : IUserRepository , simple_user_data : dict ):
        user = userUseCases.RegisterUserCase(user_repository , BcryptHashEncrypt).execute(simple_user_data)
        user_repository.session.commit()
        assert user_repository.get("id" , user.id) is not None , "Register faill"

    def test_if_register_create_a_user_with_an_exist_email(self , user_repository : IUserRepository ,simple_user : User ,simple_user_data : dict):
        user_repository.create(simple_user)
        with pytest.raises(IntegrityException):
            userUseCases.RegisterUserCase(user_repository , BcryptHashEncrypt).execute(simple_user_data)

    def test_if_register_create_a_user_with_a_short_password(self,user_repository : IUserRepository , simple_user_data : dict ):
        simple_user_data["password"] = "test"
        with pytest.raises(ValidateException):
            userUseCases.RegisterUserCase(user_repository , BcryptHashEncrypt).execute(simple_user_data)

    def test_if_register_use_case_is_returning_a_user_entitie(self,user_repository : IUserRepository , simple_user_data : dict):
        user = userUseCases.RegisterUserCase(user_repository , BcryptHashEncrypt).execute(simple_user_data)
        assert isinstance(user,User)


class TestLoginUserUseCase:

    def create_user(self , user_data : dict , repository : IUserRepository) -> User:
        data = user_data.copy()
        password = BcryptHashEncrypt.encrypt(data.pop("password"))
        user = User(**data , password=password)
        return repository.create(user)

    def test_if_login_is_returning_the_user_id(self, user_repository : IUserRepository , simple_user_data : dict ):
        user = self.create_user(simple_user_data , user_repository)
        del simple_user_data["name"]
        user_id = userUseCases.LoginUseCase(user_repository , BcryptHashEncrypt).execute(simple_user_data)
        assert user_id == user.id

    def test_if_login_is_returning_a_valid_id(self, user_repository : IUserRepository , simple_user_data : dict ):
        self.create_user(simple_user_data , user_repository)
        del simple_user_data["name"]
        user_id = userUseCases.LoginUseCase(user_repository , BcryptHashEncrypt).execute(simple_user_data)
        assert user_repository.get("id" , user_id) is not None
