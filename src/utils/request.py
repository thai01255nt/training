import json
from typing import Tuple, Dict

from flask_api import status

from src.common.responses.exceptions import BaseExceptionResponse


class RequestUtils:
    @staticmethod
    def get_json_body(request) -> Tuple[Dict, Dict]:
        request_header = request_body = {}
        # if request.content_type != "application/json":
        #     raise BaseExceptionResponse(
        #         http_code=status.HTTP_400_BAD_REQUEST,
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         message="Payload body must be json content type.",
        #     )
        try:
            if request.query_string != b"":
                request_header = request.args.to_dict()
            if request.get_data() != b"":
                request_body = json.loads(request.get_data())
        except Exception:
            raise BaseExceptionResponse(
                http_code=status.HTTP_400_BAD_REQUEST,
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Payload body must be json content type.",
            )
        return request_header, request_body

    @staticmethod
    def get_files(request):
        results = {}
        for key in request.files:
            results[key] = request.files.getlist(key)
        return results

    @staticmethod
    def get_token(request) -> str:
        token = request.headers.get("Authorization", None)
        if token is None:
            raise BaseExceptionResponse(
                http_code=status.HTTP_400_BAD_REQUEST, status_code=status.HTTP_400_BAD_REQUEST, message="Missing token."
            )
        token = token[7:]
        return token

    @staticmethod
    def get_params_from_url(request):
        return dict(request.args)
