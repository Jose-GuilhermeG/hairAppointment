from typing import Annotated
from fastapi import Depends

from src.app.application.ports.repository import IUserRepository 
from src.app.adapters.api.dependencies.db import SessionDep
from src.app.adapters.repository import UserRepositoryDb

def get_user_repository(dbSession : SessionDep)->UserRepositoryDb:
    return UserRepositoryDb(dbSession)

UserRepositoryDep = Annotated[IUserRepository , Depends(get_user_repository)]