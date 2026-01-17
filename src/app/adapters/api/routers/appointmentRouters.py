from datetime import date

from fastapi import APIRouter, status

from src.app.adapters.api.dependencies.auth import UserIdDep
from src.app.adapters.api.dependencies.repository import (
    AppointmentRepositoryDep,
    DayRepositoryDep,
)
from src.app.adapters.api.schemas.serializers import (
    AppointmentCreateIn,
    AppointmentList,
    SimpleResponse,
)
from src.app.application.use_cases.appointmentUseCases import (
    AppoinetmentData,
    GetAppointment,
    ListAppointmentsFree,
)

router = APIRouter(
    prefix="/appointment",
    tags=["Appointment"]
)

@router.get(
    '/today/free/',
    status_code=status.HTTP_200_OK,
    response_model=list[AppointmentList]
)
async def list_today_appointments_free(day_repository : DayRepositoryDep):
    today = date.today()
    appointments = ListAppointmentsFree(day_repository).execute(today)
    return [AppointmentList(started_at=appointment[0] , finish_at=appointment[1]) for appointment in appointments]

@router.get(
    "/free/",
    status_code=status.HTTP_200_OK,
    response_model=list[AppointmentList]
)
async def list_appointments_free(day_repository : DayRepositoryDep , day : date  = date.today()):
    appointments = ListAppointmentsFree(day_repository).execute(day)
    return [AppointmentList(started_at=appointment[0] , finish_at=appointment[1]) for appointment in appointments]

@router.post(
    '/{date}/',
    status_code=status.HTTP_201_CREATED,
    response_model=SimpleResponse
)
async def get_appointment( user_id : UserIdDep, repository : AppointmentRepositoryDep , day_repository : DayRepositoryDep, appointment : AppointmentCreateIn , date : date):
    request_data : AppoinetmentData = appointment.model_dump() #type: ignore
    request_data["user_id"] = int(user_id)
    GetAppointment(repository,day_repository).execute(request_data , date)

    return SimpleResponse(detail="corte agendado")
