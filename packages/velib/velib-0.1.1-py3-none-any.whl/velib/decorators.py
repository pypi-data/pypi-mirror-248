from functools import wraps
from fastapi import HTTPException, Header
from fastapi.requests import Request
import jwt


CONTENT_TYPE = 'application/json'


def content_type(request: Request):
    content_type_header = request.headers.get('Content-Type')
    if content_type_header != CONTENT_TYPE:
        raise HTTPException(status_code=400, detail="Content-Type header invalid")