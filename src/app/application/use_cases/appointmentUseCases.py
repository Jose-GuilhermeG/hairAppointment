from datetime import date, datetime
from typing import TypedDict

from src.app.application.ports.repository import IAppointmentRepository, IDayRepository
from src.app.domain.entities import Appointment
from src.app.domain.enums import HairCutEnum
from src.app.domain.exceptions import IntegrityException, UnauthorizedException


class AppoinetmentData(TypedDict , total=False):
    user_id : int
    started_at : datetime
    finish_at : datetime
    type : HairCutEnum

class ListAppointmentsFree:
    def __init__(self , day_repository : IDayRepository ):
        self.day_repository = day_repository

    def execute(self , date : date) -> list[tuple[datetime , datetime]]:
        day , appointments  = self.day_repository.get_day_appointments_by_date(date)
        return day.get_free_schedules(appointments)

class GetAppointment:
    def __init__(self ,repository : IAppointmentRepository , day_repository : IDayRepository):
        self.repository = repository
        self.day_repository = day_repository

    def execute(self, data : AppoinetmentData , day_date : date) -> Appointment:
        day , appointments  = self.day_repository.get_day_appointments_by_date(day_date)
        started_at  = data["started_at"]

        if data.get("finish_at",None) is None:
            data["finish_at"] = started_at + day.get_schedule_time()

        finish_at = data["finish_at"]

        if (started_at , finish_at) not in day.get_schedules():
            raise IntegrityException("the shcedule is invalid")


        if (started_at , finish_at) in [(appt.started_at , appt.finish_at) for appt in appointments]:
            raise IntegrityException("the schedule is already booked")

        appointment_time = finish_at - started_at

        if appointment_time < day.get_schedule_time():
            raise IntegrityException()

        appointment = Appointment.create(**data,day_id=day.id) #type: ignore
        return self.repository.create(appointment)

class DeleteAppoiment:
    def __init__(self , repository : IAppointmentRepository):
        self.repository = repository

    def execute(self , day : date , schedule : str , user_id : int) -> None:
        appoinetment = self.repository.get_appointment_by_day_and_schedule(day,schedule)
        if not appoinetment:
            raise IntegrityException("appoinetment not found")
        if appoinetment.user_id != user_id:
            raise UnauthorizedException()

        self.repository.delete_by_id(appoinetment.id) #type: ignore[arg-type]
