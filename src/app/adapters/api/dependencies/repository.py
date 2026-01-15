from typing import Annotated

from fastapi import Depends

from src.app.adapters.api.dependencies.db import SessionDep
from src.app.adapters.mapping import UserMapping
from src.app.adapters.repository import UserRepositoryDb
from src.app.application.ports.repository import IUserRepository


def get_user_repository(dbSession : SessionDep)->UserRepositoryDb:
    return UserRepositoryDb(UserMapping() , dbSession)

UserRepositoryDep = Annotated[IUserRepository , Depends(get_user_repository)]
