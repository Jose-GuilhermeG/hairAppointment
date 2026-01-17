from typing import Generic, Type

from src.app.adapters.api.schemas.models import AppointmentModel, DayModel, UserModel
from src.app.application.ports.mapping import IMapping, TEntity, TModel
from src.app.domain.entities import Appointment, Day, User


class BaseMapping(
    IMapping[TEntity , TModel],
    Generic[TEntity , TModel]
):
    _attrs : list[str] = []
    _model_convertion : Type[TModel]
    _entitie_convertion : Type[TEntity]

    def get_attrs(self , source_class ):
        model_data = {}
        for attr in self._attrs:
            model_data[attr] = getattr(source_class , attr)

        return model_data


    def convertion(self , source_class ,convertion_class):
        if source_class is None:
                return None

        if isinstance(source_class,(list , tuple , set)):
            return self.many_convertion(source_class , convertion_class)

        model_data = self.get_attrs(source_class)
        model = convertion_class(**model_data)

        if source_class.id is not None:
            model.id = source_class.id

        return model

    def many_convertion(self, source_class_list , convertion_class):
        convertion_class_list = []

        for instance in source_class_list:
            instance_data = self.get_attrs(instance)
            instance_converted = convertion_class(**instance_data)
            if instance.id is not None:
                instance_converted.id = instance.id

            convertion_class_list.append(instance_converted)

        return convertion_class_list


    def to_model(self, entitie) -> TModel | list[TModel] | None:
        return self.convertion(entitie,self._model_convertion)

    def to_entitie(self, model) -> TEntity | list[TEntity] | None:
        return self.convertion(model,self._entitie_convertion)

class UserMapping(
    BaseMapping[User , UserModel],
):
    _attrs = ["name" ,"email","password"]
    _entitie_convertion = User
    _model_convertion = UserModel

class AppointmentMapping(
    BaseMapping[Appointment , AppointmentModel],
):
    _attrs = ["user_id", "day_id" ,"started_at" , "finish_at", "type"]
    _entitie_convertion = Appointment
    _model_convertion = AppointmentModel

class DayMapping(
    BaseMapping[Day , DayModel],
):
    _attrs = ["date" , "started_at" , "finish_at"]
    _entitie_convertion = Day
    _model_convertion = DayModel
