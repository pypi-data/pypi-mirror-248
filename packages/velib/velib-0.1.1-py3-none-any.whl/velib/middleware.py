from fastapi import status
import traceback
from log import log
import sys
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from utils import dict_to_inline


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as error:
        log.error(error)
        log.error(traceback.format_exc())
        return Response("Something went wrong", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
    
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:

        http_request = {
            'Method': request.method,
            'Url': request.url.path,
            'Size': sys.getsizeof(request),
            'Ip': request.client.host,
            'Protocol': request.url.scheme,
        }

        if 'referrer' in request.headers:
            http_request['Referrer'] = request.headers.get('referrer')

        if 'user-agent' in request.headers:
            http_request['userAgent'] = request.headers.get('user-agent')

        try:
            log.debug('Request: {0}'.format(dict_to_inline(http_request)))
            return await call_next(request)
        except Exception as ex:
            log.error(f'Request failed: {ex}')
        