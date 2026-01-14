from abc import ABC , abstractmethod

class IMapping(ABC):
    @abstractmethod
    def to_model(self, entitie : object , many : bool = False) -> object | None:
        pass

    @abstractmethod
    def to_entitie(self , model : object , many : bool = False) -> object | None:
        pass
