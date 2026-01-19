from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Any, Generic, TypeVar

from src.app.application.ports.mapping import IMapping
from src.app.domain.entities import Appointment, Day, User

T = TypeVar("T")

class IRepository(
    ABC,
    Generic[T]
):
    def __init__(self , mapper : IMapping):
        self.mapper = mapper

    @abstractmethod
    def save(self , entitie : T) -> T:
        pass

    @abstractmethod
    def create(self , entitie : T) -> T:
        pass

    @abstractmethod
    def get(self , field : str , value : Any , exec : bool = True)-> T | None:
        pass

    @abstractmethod
    def all(self , exec : bool = True)-> list[T]:
        pass

    @abstractmethod
    def limit(self , limit : int , offeset : int ,exec : bool = True) -> list[T]:
        pass

    @abstractmethod
    def delete_by_id(self , id : int)->None:
        pass



class IAppointmentRepository(
    IRepository[Appointment]
):
    @abstractmethod
    def get_appointment_by_day_and_schedule(self,day : date , schedule : str) -> Appointment:
        pass

    @abstractmethod
    def get_appointments_by_day(self,day : date)->list[Appointment]:
        pass

    @abstractmethod
    def delet_appointment_by_date_and_schedule(self , day : date , schedule : datetime)->None:
        pass

class IUserRepository(
    IRepository[User]
):

    appointment_mapping : IMapping

    @abstractmethod
    def get_user_permissions_by_id(self, user_id : int)->list[str]:
        pass

    @abstractmethod
    def get_user_with_appointment_by_id(self,User_id : int)->list[Appointment]:
        pass

class IDayRepository(
    IRepository[Day]
):
    appointment_mapping : IMapping

    @abstractmethod
    def get_day_appointments_by_date(self , date : date ) -> tuple[Day,list[Appointment]]:
        pass
