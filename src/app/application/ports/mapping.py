from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")

class IMapping(ABC , Generic[T]):
    @abstractmethod
    def to_model(self, entitie : T ) -> T | None:
        pass

    @abstractmethod
    def to_entitie(self , model : T ) -> T | None:
        pass
