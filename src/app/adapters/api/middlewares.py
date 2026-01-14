from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from sqlmodel import Session
from types import FunctionType

from src.app.adapters.api.dependencies.db import engine

class DbSessionMiddleware(
    BaseHTTPMiddleware
):
    async def dispatch(self,request: Request, call_next : FunctionType):
        response = None
        with Session(engine) as session:
            request.state.db = session
            try:
                response = await call_next(request)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close() 
        return response
