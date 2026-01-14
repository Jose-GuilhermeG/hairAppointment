from src.app.application.ports.repository import IUserRepository
from src.app.application.ports.hashsEncrypt import IHashEncrypt
from src.app.domain.entities import User
from src.app.domain.exceptions import IntegrityException , ValidateException


class RegisterUserCase:
    def __init__(self , repository : IUserRepository , passwordHash : IHashEncrypt):
        self.repository = repository
        self.passwordHash = passwordHash

    async def execute(self , data : dict[str , str])->User:
        raw_password = data.get("password" , None)

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

    def execute(self, user : User ,new_password : str) -> None:
        hashed_pass = self.passwordHash.encrypt(new_password)
        user.password = hashed_pass
        self.repository.save(user)
