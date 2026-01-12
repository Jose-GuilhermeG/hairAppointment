from abc import ABC , abstractmethod

class IRepository(
    ABC
):

    @abstractmethod
    def save(self , data : dict[str,any]):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def get(self , field : str , value : any):
        pass

    @abstractmethod
    def filter(self):
        pass

class IAppoinmentRepository(
    IRepository
):
    pass

class IUserRepository(
    IRepository
):
    pass
