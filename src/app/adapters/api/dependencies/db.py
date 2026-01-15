from typing import Annotated

from fastapi import Depends, Request
from sqlmodel import Session, create_engine

from src.configs.settings import DATABASE_URI

engine = create_engine(DATABASE_URI)

def get_session(request : Request):
    return request.state.db

SessionDep = Annotated[Session , Depends(get_session)]
