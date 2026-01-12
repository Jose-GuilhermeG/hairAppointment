from sqlmodel import Session
from typing import Annotated
from fastapi import Depends

from src.configs.settings import DATABASE_URI

from sqlmodel import Session , create_engine

engine = create_engine(DATABASE_URI)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session , Depends(get_session)]