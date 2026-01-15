from abc import ABC , abstractmethod

from src.app.domain.entities import User
from src.app.application.ports.mapping import IMapping

class IRepository(
    ABC
):
    def __init__(self , mapper : IMapping):
        self.mapper = mapper

    @abstractmethod
    def save(self , entitie : object):
        pass

    @abstractmethod
    def create(self , entitie : object):
        pass

    @abstractmethod
    def get(self , field : str , value : any , exec : bool = True):
        pass

    @abstractmethod
    def all(self , exec : bool = True):
        pass

    @abstractmethod
    def limit(self , limit : int , offeset : int ,exec : bool = True):
        pass

    @abstractmethod
    def delete_by_id(self , id : int)->None:
        pass

    @abstractmethod
    def exec(self , query : str):
        pass


class IAppoinmentRepository(
    IRepository
):
    pass


class IUserRepository(
    IRepository
):

    @abstractmethod
    def get(self, field, value, exec = True)->User:
        pass

    @abstractmethod
    def all(self, exec = True)->list[User]:
        pass

    @abstractmethod
    def limit(self, limit, offeset, exec = True)->list[User]:
        pass

    @abstractmethod
    def save(self , entitie : User ) -> User:
        pass

    @abstractmethod
    def create(self , entitie : User ) -> User:
        pass
