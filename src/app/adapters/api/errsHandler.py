from fastapi import  Request , status
from fastapi.responses import JSONResponse
from src.app.domain.exceptions import IntegrityException

async def integrity_exception_handler(request : Request , exc : IntegrityException)->JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"err" : exc.message}
    )

async def unauthorize_exception_handler(request : Request , exc : IntegrityException)->JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"err" : exc.message}
    )
async def internal_exception_err(request : Request , exc : Exception)->JSONResponse:
    """used when the exception is not known"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"err" : "internal err"}
    )
