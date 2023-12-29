from typing import Union
from pydantic import BaseModel
from fastapi.responses import Response as _Response
from .crypto import get_random_string
from datetime import datetime
import string
import json


class Response(_Response):
    status_code = 200
    media_type = 'application/json'
    
    def __init__(self, *args, **kwargs):
        super().__init__(ResponseModel(*args, **kwargs).make_response())


class ResponseModel(BaseModel):
    requestId: str = get_random_string(length=32, allowed_chars=string.ascii_lowercase + string.digits)
    success: bool = True
    error: int = 0
    detail: Union[list, str, int] = None
    timestamp: float = datetime.timestamp(datetime.now())
    
    def __init__(self, *args, **kwargs):
        super().__init__()        
        self.__dict__.update(kwargs)
        
        for item in args:
            if isinstance(item, dict):                
                self.__dict__.update(item)
            elif isinstance(item, str):
                self.detail = item
            else:
                for key, value in item.__dict__.items():
                    setattr(self, key, value)
    
    def __str__(self):
        return self.make_response()
    
    def make_response(self):
        if self.detail and isinstance(self.detail, str):
            self.detail = self.detail.replace("\n", " ")
        return json.dumps(self.__dict__)
        #return self.model_dump_json()
