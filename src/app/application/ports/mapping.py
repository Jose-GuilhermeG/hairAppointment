from abc import ABC, abstractmethod
from typing import Generic, Sequence, TypeVar

TEntity = TypeVar("TEntity")
TModel = TypeVar("TModel")

class IMapping(ABC , Generic[TEntity , TModel]):
    @abstractmethod
    def to_model(self, entitie : TEntity | Sequence[TEntity] ) -> TModel | list[TModel] | None:
        pass

    @abstractmethod
    def to_entitie(self , model : TModel | Sequence[TModel] ) -> TEntity | list[TEntity] | None:
        pass
