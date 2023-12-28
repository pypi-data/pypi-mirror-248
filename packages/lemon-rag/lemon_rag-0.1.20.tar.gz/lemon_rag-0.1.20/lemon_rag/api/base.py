import uuid
from typing import Callable, Union, Type, Dict

import sanic.request
from pydantic import BaseModel, ValidationError
from sanic import response

from lemon_rag.utils import response_utils
from lemon_rag.utils.response_utils import ReturnCode

PydanticRequestHandler_F = Callable[[BaseModel], response.HTTPResponse]
Handler_F = Callable[[sanic.request.Request], Union[response.HTTPResponse, response.StreamingHTTPResponse]]


def handle_request_with_pydantic(request_type: Type[BaseModel]) -> Callable[[PydanticRequestHandler_F], Handler_F]:
    def decorator(func: PydanticRequestHandler_F) -> Handler_F:
        def inner(request: sanic.request.Request) -> Union[response.HTTPResponse, response.StreamingHTTPResponse]:
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


ai_assistant_api_mapping: Dict[str, Handler_F] = {}


def add_route(path, handler: Handler_F):
    ai_assistant_api_mapping[path] = handler


def handle_all_api(
        request: sanic.request.Request,
        sub_path: str
) -> Union[response.HTTPResponse, response.StreamingHTTPResponse]:
    rid = uuid.uuid4().hex
    handler = ai_assistant_api_mapping.get(sub_path)
    if not handler:
        return response.text(f"Not Found\nrid:{rid}", status=404)
    res = handler(request)
    res.headers.setdefault("rid", rid)
    return res
