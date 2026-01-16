from src.app.adapters.api.schemas.models import UserModel
from src.app.application.ports.mapping import IMapping
from src.app.domain.entities import User


class UserMapping(
    IMapping[User]
):
    def to_model(self, entitie : User | None | list[User]):
        if entitie is None:
            return None

        if isinstance(entitie,(list , tuple , set)):
            return self.model_many_convertion(entitie)

        user_model = UserModel(name = entitie.name , email = entitie.email , password = entitie.password)

        if entitie.id is not None:
            user_model.id = entitie.id

        return user_model

    def to_entitie(self, model):
        if model is None:
            return None

        if isinstance(model,(list , tuple , set)):
            return self.entitie_many_convertion(model)

        user_entitie = User(name = model.name , email = model.email , password = model.password)

        if model.id is not None:
              user_entitie.id = model.id

        return user_entitie

    def entitie_many_convertion(self,model : list[UserModel]) -> list[User]:
        entitie_user_list = []

        if not isinstance(model, (set , list , tuple)):
            raise TypeError("models must be a interable")

        for user in model:
           user_entitie = User(name = user.name , email = user.email , password = user.password)
           if user.id is not None:
               user_entitie.id = user.id

           entitie_user_list.append(user_entitie)

        return entitie_user_list

    def model_many_convertion(self,entities : list[User])->list[UserModel]:
        model_user_list = []

        if not isinstance(entities, (set , list , tuple)):
            raise TypeError("entities must be a interable")

        for user in entities:
            user_model = UserModel(name = user.name , email = user.email , password = user.password)
            if user.id is not None:
                user_model.id = user.id

            model_user_list.append(user_model)

        return model_user_list
