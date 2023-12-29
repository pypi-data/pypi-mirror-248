from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette.requests import Request
from . response import Response


async def http_error_handler(_: Request, exc: HTTPException) -> Response:
    response_data = {'success': False, 'error': 1, 'detail': exc.detail}
    res = Response(response_data)
    res.status_code = exc.status_code
    return res


async def validation_error_handler(_: Request, exc: RequestValidationError,) -> Response:
    response_data = {        
        'success': False,
        'error': 1,
        'detail': exc.errors(),        
    }
    if exc.body:
        response_data['body'] = exc.body
    res = Response(response_data)
    res.status_code = 422
    return res


__all__ = ['http_error_handler', 'validation_error_handler']
