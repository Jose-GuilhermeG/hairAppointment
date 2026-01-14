from fastapi import FastAPI
from sqlmodel import SQLModel
from contextlib import asynccontextmanager

from src.configs.settings import DEBUG
from src.app.adapters.api.routers import userRouters
from src.app.adapters.api.dependencies.db import engine
from src.app.adapters.api.errsHandler import integrity_exception_handler , internal_exception_err , unauthorize_exception_handler , validate_exception_handler
from src.app.domain.exceptions import IntegrityException , UnauthorizedException , ValidateException

@asynccontextmanager
async def lifespan(app :  FastAPI):
    SQLModel.metadata.create_all(engine)

    yield

app = FastAPI(
    debug=DEBUG,
    lifespan=lifespan
)

app.include_router(
    router=userRouters.router
)

app.add_exception_handler(ValidateException, validate_exception_handler)
app.add_exception_handler(IntegrityException , integrity_exception_handler)
app.add_exception_handler(UnauthorizedException , unauthorize_exception_handler)
app.add_exception_handler(Exception , internal_exception_err)
