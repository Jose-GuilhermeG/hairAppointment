import pytest
from sqlmodel import Session , create_engine , SQLModel

from src.app.domain.entities import User
from src.app.application.ports.repository import IUserRepository
from src.app.adapters.repository import UserRepositoryDb
from src.app.adapters.mapping import UserMapping
from src.configs.settings import TEST_DATABASE_URI

engine = create_engine(TEST_DATABASE_URI)

@pytest.fixture
def simple_user_data()->dict[str,str]:
    return {"name" : "Test user" , "email" : "emailTest@exemple.com" , "password" : "testepassword" }

@pytest.fixture
def simple_user(simple_user_data) -> User:
    user = User(**simple_user_data)
    return user

@pytest.fixture
def session():
    with Session(engine) as dbSession:
        SQLModel.metadata.create_all(engine)
        yield dbSession
        dbSession.close()
        SQLModel.metadata.drop_all(engine)

@pytest.fixture
def user_mapping() -> UserMapping:
    return UserMapping()

@pytest.fixture
def user_repository(session , user_mapping) -> IUserRepository:
    return UserRepositoryDb(user_mapping,session)
