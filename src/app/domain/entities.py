from src.app.domain.enums import HairCutEnum
from dataclasses import dataclass
from datetime import date

@dataclass
class User:
    id : int | None
    name : str
    email : str
    password : str

    def __repr__(self):
        return f"{self.name}"

@dataclass
class Appoinment:
    id : int | None
    user_id : int
    appoinment_date : date
    type : HairCutEnum
