import json
import os

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.api import api_router
from src.common.consts import MessageConsts, CommonConsts
from src.common.responses.exceptions import BaseExceptionResponse
from src.utils.logger import LOGGER

app = FastAPI(
    title="training",
    description="Welcome to API documentation",
    # root_path="/api/v1",
    docs_url="/docs" if CommonConsts.DEBUG else None,
    # openapi_url="/docs/openapi.json",
    redoc_url="/docs" if CommonConsts.DEBUG else None,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def exception_handler(request: Request, exception: RequestValidationError):
    errors = {}
    for error in exception.errors():
        field = error["loc"][-1]
        if field not in error:
            errors[field] = []
        errors[field].append(error["msg"])
    exception = BaseExceptionResponse(
        http_code=400,
        status_code=400,
        message=MessageConsts.BAD_REQUEST,
        errors=errors,
    )
    error_response = exception.to_dict()
    LOGGER.error(json.dumps(error_response))
    return JSONResponse(
        status_code=exception.http_code,
        content=error_response,
    )


@app.exception_handler(Exception)
async def exception_handler(request: Request, exception):
    if isinstance(exception, BaseExceptionResponse):
        error_response = exception.to_dict()
    else:
        errors = (
            None if not CommonConsts.DEBUG else {"key": MessageConsts.INTERNAL_SERVER_ERROR, "message": str(exception)}
        )
        exception = BaseExceptionResponse(
            http_code=500,
            status_code=500,
            message=MessageConsts.INTERNAL_SERVER_ERROR,
            errors=errors,
        )
        error_response = exception.to_dict()
    LOGGER.error(json.dumps(error_response))
    return JSONResponse(
        status_code=exception.http_code,
        content=error_response,
    )


app.include_router(prefix="/api/v1", router=api_router)
