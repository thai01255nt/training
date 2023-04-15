import json
import os

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from engine.api import api_router
from engine.common.consts import MessageConsts
from engine.common.responses.exceptions import BaseExceptionResponse
from engine.utils.logger import LOGGER

app = FastAPI(
    title="training",
    description="Welcome to API documentation",
    # root_path="/api/v1",
    # docs_url=None,
    # openapi_url="/docs/openapi.json",
    redoc_url="/docs",
)


@app.exception_handler(RequestValidationError)
async def exception_handler(request: Request, exception: RequestValidationError):
    errors = {}
    for error in exception.errors():
        ref_error = errors
        field = None
        previous_error = None
        for i in range(len(error["loc"])):
            field = error["loc"][i]
            if field not in ref_error:
                ref_error[field] = {}
            previous_error = ref_error
            ref_error = ref_error[field]
        if isinstance(ref_error, list):
            ref_error.append(error["msg"])
        elif field is not None:
            previous_error[field] = [error["msg"]]
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
            None if not os.environ["DEBUG"] else {"key": MessageConsts.INTERNAL_SERVER_ERROR, "message": str(exception)}
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
