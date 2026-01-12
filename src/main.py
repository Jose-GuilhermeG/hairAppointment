from fastapi import FastAPI
from sqlmodel import SQLModel

from src.configs.settings import DEBUG
from src.app.adapters.api.routers import userRouters
from src.app.adapters.api.dependencies.db import engine
from src.app.adapters.api.errsHandler import integrity_exception_handler , internal_exception_err , unauthorize_exception_handler
from src.app.domain.exceptions import IntegrityException , UnauthorizedException

app = FastAPI(
    debug=DEBUG
)

app.include_router(
    router=userRouters.router
)

app.add_exception_handler(IntegrityException , integrity_exception_handler)
app.add_exception_handler(UnauthorizedException , unauthorize_exception_handler)
app.add_exception_handler(Exception , internal_exception_err)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
