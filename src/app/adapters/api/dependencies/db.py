from sqlmodel import Session
from typing import Annotated
from fastapi import Depends , Request

from src.configs.settings import DATABASE_URI

from sqlmodel import create_engine

engine = create_engine(DATABASE_URI)

def get_session(request : Request):
    return request.state.db

SessionDep = Annotated[Session , Depends(get_session)]
