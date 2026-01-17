from sqlalchemy import delete
from sqlalchemy.orm import selectinload
from sqlmodel import Session, SQLModel, select

from src.app.adapters.api.schemas.models import (
    AppointmentModel,
    DayModel,
    PermissionModel,
    UserModel,
    UserPermissionModel,
)
from src.app.application.ports.repository import (
    IAppointmentRepository,
    IDayRepository,
    IRepository,
    IUserRepository,
)
from src.app.domain.exceptions import IntegrityException


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

    def __init__(self, mapper, session , appointment_mapping):
        super().__init__(mapper, session)
        self.appointment_mapping = appointment_mapping

    def get_user_permissions_by_id(self, user_id):
        query = select(PermissionModel).join(UserPermissionModel).join(self._model).where(self._model.id == user_id)
        permissions = self.exec(query).all()
        return [permission.name for permission in permissions]

    def get_user_with_appointment_by_id(self, user_id):
        query =select(self._model).options(selectinload(self._model.appointments)).where(self._model.id == user_id)
        user = self.exec(query).first()
        if user is None:
            raise IntegrityException("user don't found")
        return self.appointment_mapping.to_entitie(user.appointments)



class AppointmentRepositoryDb(
    BaseRepositoryDb,
    IAppointmentRepository
):
    _model = AppointmentModel

class DayRepositoryDb(
    BaseRepositoryDb,
    IDayRepository
):
    _model = DayModel

    def __init__(self, mapper, session,appoinment_mapping):
        super().__init__(mapper, session)
        self.appointment_mapping = appoinment_mapping

    def get_day_appointments_by_date(self, date):
        query = select(DayModel).options(selectinload(DayModel.appointments)).where(DayModel.date == date)
        day = self.exec(query).first()

        if not day:
            raise IntegrityException("Day don't found")

        return self.mapper.to_entitie(day),self.appointment_mapping.to_entitie(day.appointments)
