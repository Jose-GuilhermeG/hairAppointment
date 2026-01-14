from fastapi import Header , Depends
from typing import Annotated
from uuid import uuid4

from src.configs.settings import  SESSION_EXPIRE_TIME
from src.app.application.ports.repository import IUserRepository
from src.app.application.ports.hashsEncrypt import IEncryptData
from src.app.domain.exceptions import UnauthorizedException , IntegrityException
from src.app.adapters.api.schemas.models import UserModel
from src.app.adapters.api.dependencies.services import Redis , redis
from src.app.adapters.api.dependencies.repository import UserRepositoryDep
from src.app.adapters.hashEncrypt import Base64Encrypt


class Auth:
    def __init__(self , dataPersistence : Redis , repository : IUserRepository ,encrypt : IEncryptData , deathList : str = "deathlist" ):
        self.dataPersistence = dataPersistence
        self.repository = repository
        self.encrypt = encrypt
        self.deathList = deathList

    def get_user_id(self,token : str)-> int | None:
        decode_token = self.encrypt.decode(token)

        if decode_token is None:
            raise IntegrityException("Invalid token")

        user_id = self.dataPersistence.get(decode_token)
        is_token_on_deathList = bool(self.dataPersistence.sismember(self.deathList, decode_token))
        if user_id is None or is_token_on_deathList:
            raise UnauthorizedException("User don't found")
        return user_id

    def get_user(self , user_id : int) -> UserModel:
        return self.repository.get("id",user_id)

    def create_user_token(self , user_id : int , expire_time : int = SESSION_EXPIRE_TIME)->str:
        token = "user:" + str(uuid4())
        self.dataPersistence.set(token , user_id ,expire_time )
        return self.encrypt.encrypt(token)

    def add_token_to_deathlist(self,token : str):
        decode_token = self.encrypt.decode(token)

        if decode_token is None:
            raise IntegrityException("Invalid token")

        self.dataPersistence.sadd(self.deathList , decode_token)

async def get_auth( repository : UserRepositoryDep) -> Auth:
    return Auth(redis , repository , Base64Encrypt)

AuthDep = Annotated[Auth , Depends(get_auth)]
SessionIdDep = Annotated[str , Header()]

async def login_required(session_id : SessionIdDep , auth_manager : AuthDep)->UserModel:
    user_id = auth_manager.get_user_id(session_id)
    return user_id


UserIdDep = Annotated[int , Depends(login_required)]
