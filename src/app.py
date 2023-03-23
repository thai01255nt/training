import json
import os

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from src.api import api_router
from src.common.consts import MessageConsts
from src.common.responses.exceptions import BaseExceptionResponse
from src.utils.logger import LOGGER

app = FastAPI(
    title="training",
    description="Welcome to API documentation",
    # root_path="/api/v1",
    # docs_url=None,
    # openapi_url="/docs/openapi.json",
    redoc_url="/docs",
)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exception: Exception):
    if isinstance(exception, BaseExceptionResponse):
        error_response = exception.to_dict()
        LOGGER.error(json.dumps(error_response))
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
    return JSONResponse(
        status_code=exception.http_code,
        content=error_response,
    )


app.include_router(prefix="/api/v1", router=api_router)
