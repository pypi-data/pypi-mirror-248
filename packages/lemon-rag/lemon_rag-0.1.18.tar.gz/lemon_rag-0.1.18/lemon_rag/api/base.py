from typing import Callable, Union, Type

import sanic.request
from pydantic import BaseModel, ValidationError
from sanic import response

from lemon_rag.utils import response_utils
from lemon_rag.utils.response_utils import ReturnCode

PydanticRequestHandler_F = Callable[[BaseModel], response.HTTPResponse]
Handler_F = Callable[[sanic.request.Request], Union[response.HTTPResponse]]


def handle_request_with_pydantic(request_type: Type[BaseModel]) -> Callable[[PydanticRequestHandler_F], Handler_F]:
    def decorator(func: PydanticRequestHandler_F) -> Handler_F:
        def inner(request: sanic.request.Request) -> Union[response.HTTPResponse]:
            try:
                structured_req = request_type.parse_obj(request.json)
            except ValidationError as e:
                return response_utils.response(
                    code=ReturnCode.invalid_json, data={"errors": e.errors()}
                )
            res = func(structured_req)
            return res

        return inner

    return decorator
