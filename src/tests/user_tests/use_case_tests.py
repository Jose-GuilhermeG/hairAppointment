import pytest

from src.app.application.ports.hashsEncrypt import IEncryptData
from src.app.application.ports.repository import IUserRepository
from src.app.application.use_cases import userUseCases
from src.app.domain.entities import User
from src.app.domain.exceptions import IntegrityException, ValidateException
from src.tests.user_tests.user_fixtures import get_hash_encypt, hash_encrypt


@pytest.fixture
def register_use_case(user_repository : IUserRepository , hash_encrypt : IEncryptData ):
    return userUseCases.RegisterUserCase(user_repository , hash_encrypt)

@pytest.fixture
def login_use_case(user_repository : IUserRepository , hash_encrypt : IEncryptData ) :
    return userUseCases.LoginUseCase(user_repository , hash_encrypt)

@pytest.fixture
def user_detail_use_case(user_repository):
    return userUseCases.UserDetailsUseCase(user_repository)

class TestRegisterUserCase:

    def test_if_register_is_create_a_user(self,user_repository : IUserRepository , simple_user_data : dict , hash_encrypt : IEncryptData ):
        user = userUseCases.RegisterUserCase(user_repository , hash_encrypt).execute(simple_user_data)
        user_repository.session.commit()
        assert user_repository.get("id" , user.id) is not None , "Register faill"

    def test_if_register_create_a_user_with_an_exist_email(self , register_use_case , user_repository : IUserRepository ,simple_user : User ,simple_user_data : dict):
        user_repository.create(simple_user)
        with pytest.raises(IntegrityException):
            register_use_case.execute(simple_user_data)

    def test_if_register_create_a_user_with_a_short_password(self,register_use_case, simple_user_data : dict ):
        simple_user_data["password"] = "test"
        with pytest.raises(ValidateException):
            register_use_case.execute(simple_user_data)

    def test_if_register_use_case_is_returning_a_user_entitie(self,register_use_case , simple_user_data : dict):
        user = register_use_case.execute(simple_user_data)
        assert isinstance(user,User)


class TestLoginUserUseCase:
    login_user_data = {"email" : "testEmail@exemple.com" , "password" : "testPassword"}

    def setup_method(self):
        data = self.login_user_data.copy()
        data["name"] = "Test User"
        password = get_hash_encypt().encrypt(data.pop("password"))

        self.user = User(**data , password=password)

    def test_if_login_is_returning_the_user_id(self,login_use_case, user_repository : IUserRepository):
        user = user_repository.create(self.user)
        user_id = login_use_case.execute(self.login_user_data)
        assert user_id == user.id

    def test_if_login_is_returning_a_valid_id(self,login_use_case, user_repository : IUserRepository):
        user_repository.create(self.user)
        user_id = login_use_case.execute(self.login_user_data)
        assert user_repository.get("id" , user_id) is not None

    def test_login_with_an_not_register_user(self , login_use_case):
        with pytest.raises(IntegrityException):
            login_use_case.execute(self.login_user_data)

    def test_login_with_empty_and_none_password(self , login_use_case , user_repository : IUserRepository):
        user_repository.create(self.user)
        data = self.login_user_data.copy()
        data["password"] = ""
        with pytest.raises(ValidateException) :
            login_use_case.execute(data)

        data["password"] = None

        with pytest.raises(ValidateException):
            login_use_case.execute(data)

class TestUserDetailUseCase:

    def test_detail_with_invalid_id(self,user_detail_use_case):
        id = 1
        with pytest.raises(IntegrityException):
            user_detail_use_case.execute(id)

    def test_if_detail_is_retuning_correct_data(self,user_detail_use_case,user_repository : IUserRepository,simple_user : User):
        user = user_repository.create(simple_user)
        returned_data  = user_detail_use_case.execute(user.id)
        assert user != returned_data
