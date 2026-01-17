from contextlib import asynccontextmanager
from datetime import date as Date
from datetime import datetime, timedelta
from logging import INFO, FileHandler, StreamHandler, basicConfig, getLogger

from fastapi import FastAPI
from sqlmodel import Session, SQLModel

from src.app.adapters.api.dependencies.db import engine
from src.app.adapters.api.errsHandler import (
    integrity_exception_handler,
    internal_exception_err,
    unauthorize_exception_handler,
    validate_exception_handler,
)
from src.app.adapters.api.middlewares import DbSessionMiddleware
from src.app.adapters.api.routers import appointmentRouters, userRouters
from src.app.adapters.api.schemas.models import DayModel
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


#temp
def create_days():
    with Session(engine) as session:
        year = datetime.now().year
        data_inicial = Date(year, 1, 1)
        data_final = Date(year, 12, 31)

        while data_inicial <= data_final:
            started_hour = datetime(year, data_inicial.month, data_inicial.day, hour=7, minute=0, second=0, microsecond=0)
            finish_hour = datetime(year, data_inicial.month, data_inicial.day, hour=20, minute=0, second=0, microsecond=0)
            day = DayModel(date=data_inicial, started_at=started_hour, finish_at=finish_hour)
            session.add(day)
            data_inicial = data_inicial + timedelta(1)

        session.commit()

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

    #create_days()

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
app.include_router(
    router=appointmentRouters.router
)

app.add_exception_handler(ValidateException, validate_exception_handler)
app.add_exception_handler(IntegrityException , integrity_exception_handler)
app.add_exception_handler(UnauthorizedException , unauthorize_exception_handler)
app.add_exception_handler(Exception , internal_exception_err)

app.add_middleware(DbSessionMiddleware)
