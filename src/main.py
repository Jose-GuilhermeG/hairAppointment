from contextlib import asynccontextmanager
from logging import INFO, FileHandler, StreamHandler, basicConfig, getLogger

from fastapi import FastAPI
from sqlmodel import SQLModel

from src.app.adapters.api.dependencies.db import engine
from src.app.adapters.api.errsHandler import (
    integrity_exception_handler,
    internal_exception_err,
    unauthorize_exception_handler,
    validate_exception_handler,
)
from src.app.adapters.api.middlewares import DbSessionMiddleware
from src.app.adapters.api.routers import userRouters
from src.app.domain.exceptions import (
    IntegrityException,
    UnauthorizedException,
    ValidateException,
)
from src.configs.settings import (
    DEBUG,
    LOG_DATE_FORMAT,
    LOG_FILE,
    LOG_FILE_MODE,
    LOG_FORMAT,
    SYSTEM_DESCRIPTION,
    SYSTEM_NAME,
    SYSTEM_VERSION,
)


@asynccontextmanager
async def lifespan(app :  FastAPI):
    basicConfig(
        level=INFO,
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
        handlers=[
            StreamHandler(),
            FileHandler(
                filename=LOG_FILE,
                mode = LOG_FILE_MODE
            )
        ]
    )

    logger = getLogger(__name__)
    logger.info("Logs were init")

    SQLModel.metadata.create_all(engine)
    logger.info("models created")

    yield

app = FastAPI(
    title=SYSTEM_NAME,
    version=SYSTEM_VERSION,
    description=SYSTEM_DESCRIPTION,
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

app.add_middleware(DbSessionMiddleware)
