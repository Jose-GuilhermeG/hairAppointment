from sqlmodel import select

from src.app.adapters.api.schemas.models import UserModel
from src.app.domain.entities import User
from src.app.application.ports.repository import IUserRepository

from sqlmodel import Session


class UserRepositoryDb(IUserRepository):
    def __init__(self , session : Session):
        self.session = session

    def create(self , user : User)->UserModel:
        userModel = UserModel(name=user.name,email=user.email,password=user.password)
        self.session.add(userModel)
        return userModel

    def get(self , field , value) -> UserModel:
        query = select(UserModel).where(getattr(UserModel , field) == value)
        return self.session.exec(query).first()

    def save(self , user : UserModel) -> UserModel:
        self.session.add(user)
        return user

    def delete(self , user : UserModel)->None:
        return self.session.delete(user)
