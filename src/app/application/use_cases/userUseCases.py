from src.app.application.ports.repository import IUserRepository
from src.app.application.ports.hashsEncrypt import IHashEncrypt
from src.app.domain.entities import User
from src.app.domain.exceptions import IntegrityException , ValidateException


class RegisterUserCase:
    def __init__(self , repository : IUserRepository , passwordHash : IHashEncrypt):
        self.repository = repository
        self.passwordHash = passwordHash

    async def execute(self , data : dict[str , str])->User:
        raw_password = data.pop("password")

        if raw_password is None or len(raw_password) < 8 :
            raise ValidateException("'password' lenght can't be less then 8")

        password = self.passwordHash.encrypt(raw_password)
        user = User(**data , password=password)
        if self.repository.get("email" , user.email):
            raise IntegrityException("An user with that email alright exists")

        return self.repository.create(user)

class LoginUseCase:
    def __init__(self , repository : IUserRepository , passwordHash : IHashEncrypt):
       self.repository = repository
       self.passwordHash = passwordHash

    def execute(self , data : dict[str,str])->int:
        user = self.repository.get("email" ,data.get("email",None))
        if not user:
            raise IntegrityException("Doesn't user found with that email")

        if not self.passwordHash.verify(data.get("password",None),user.password):
            raise IntegrityException("Incorrect password")

        return user.id

class SetPasswordUseCase:
    def __init__(self , repository : IUserRepository , passwordHash : IHashEncrypt):
       self.repository = repository
       self.passwordHash = passwordHash

    def execute(self, user_id : int ,new_password : str) -> None:
        user = self.repository.get("id" , user_id)
        hashed_pass = self.passwordHash.encrypt(new_password)
        user.password = hashed_pass
        self.repository.save(user)

class UserDetailsUseCase:
    def __init__(self , repository : IUserRepository):
       self.repository = repository

    def execute(self,user_id : int) -> User:
        return self.repository.get("id",user_id)

class ListUsersUseCase:
    def __init__(self , repository : IUserRepository):
        self.repository = repository

    def execute(self) -> list[User]:
        return self.repository.all()

class UpdateUserUseCase:
    def __init__(self , repository : IUserRepository):
        self.repository = repository

    def execute(self , user_id : int ,data : dict[str , str]) -> User:
        user = self.repository.get("id" , user_id)

        for key , value in data.items():
            if hasattr(user,key):
                setattr(user,key,value)

        return self.repository.save(user)

class DeleteUserUseCase:
    def __init__(self , repository : IUserRepository):
        self.repository = repository

    def execute(self,user_id : int)->None:
        self.repository.delete_by_id(user_id)
