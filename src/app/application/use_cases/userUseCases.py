from src.app.application.ports.repository import IUserRepository
from src.app.application.ports.hashsEncrypt import IHashEncrypt
from src.app.domain.entities import User
from src.app.domain.exceptions import IntegrityException


class RegisterUserCase:
    def __init__(self , repository : IUserRepository , passwordHash : IHashEncrypt):
        self.repository = repository
        self.passwordHash = passwordHash

    async def execute(self , data : dict[str , str])->User:
        password = self.passwordHash.encrypt(data.pop("password"))
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

class SetPassword:
    def __init__(self , repository : IUserRepository , passwordHash : IHashEncrypt):
       self.repository = repository
       self.passwordHash = passwordHash
    
    