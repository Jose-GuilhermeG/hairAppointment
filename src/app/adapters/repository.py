from sqlalchemy import delete
from sqlmodel import Session, SQLModel, select

from src.app.adapters.api.schemas.models import UserModel
from src.app.application.ports.repository import IRepository, IUserRepository


class BaseRepositoryDb(IRepository):
    _model : SQLModel = None

    def __init__(self, mapper , session : Session):
        super().__init__(mapper)
        self.session = session

    def save(self, entitie):
        model = self.mapper.to_model(entitie)
        self.session.merge(model)
        return self.mapper.to_entitie(model)

    def get(self, field, value, exec = True):
        query = select(self._model).where(getattr(self._model , field) == value)

        if exec:
            return self.mapper.to_entitie(self.exec(query).first())

        return query

    def create(self, entitie):
        model = self.mapper.to_model(entitie)
        self.session.add(model)
        self.session.flush()
        return self.mapper.to_entitie(model)

    def delete_by_id(self, id):
        statement = delete(self._model).where(self._model.id == id)
        self.exec(statement)
        self.session.flush()

    def all(self, exec = True):
        query = select(self._model)
        if exec:
            return self.mapper.to_entitie(self.exec(query).all())

        return query

    def limit(self, limit, offeset, exec = True):
        query = select(self._model).limit(limit).offset(offeset)

        if exec:
            return self.mapper.to_entitie(self.exec(query).all())

        return query

    def exec(self, query):
        return self.session.exec(query)



class UserRepositoryDb(
    BaseRepositoryDb,
    IUserRepository,
):
    _model = UserModel
