from typing import Annotated

from fastapi import Depends

from src.app.adapters.api.dependencies.db import SessionDep
from src.app.adapters.mapping import AppointmentMapping, DayMapping, UserMapping
from src.app.adapters.repository import (
    AppointmentRepositoryDb,
    DayRepositoryDb,
    UserRepositoryDb,
)
from src.app.application.ports.repository import (
    IAppointmentRepository,
    IDayRepository,
    IUserRepository,
)


def get_user_repository(dbSession : SessionDep)->IUserRepository:
    return UserRepositoryDb(UserMapping(), dbSession , AppointmentMapping())

UserRepositoryDep = Annotated[IUserRepository , Depends(get_user_repository)]

def get_day_repository(dbSession : SessionDep)->IDayRepository:
    return DayRepositoryDb(DayMapping() , dbSession , AppointmentMapping())

DayRepositoryDep = Annotated[IDayRepository,Depends(get_day_repository)]

def get_appointment_repository(dbSession : SessionDep)->IAppointmentRepository:
    return AppointmentRepositoryDb(AppointmentMapping(),dbSession )

AppointmentRepositoryDep = Annotated[IAppointmentRepository,Depends(get_appointment_repository)]
