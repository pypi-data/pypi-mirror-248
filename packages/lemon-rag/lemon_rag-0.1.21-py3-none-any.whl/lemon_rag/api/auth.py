import time
from typing import Optional

import sanic.request
from playhouse.shortcuts import model_to_dict
from pydantic import BaseModel

from lemon_rag.api.base import handle_request_with_pydantic, add_route
from lemon_rag.core.executor_pool import submit_streaming_task
from lemon_rag.lemon_models import models
from lemon_rag.utils import log
from lemon_rag.utils.response_utils import response, stream, ReturnCode


def hello_world(request: sanic.request.Request):
    return response(message="Hello world!")


def hello_stream(request: sanic.request.Request):
    def generator():
        for line in ["aaaaa", "bbbbb", "ccccc", "ddddd"]:
            yield line
            time.sleep(1)

    queue = submit_streaming_task(generator())

    return stream(queue)


class RegisterRequest(BaseModel):
    username: str
    password: str
    mobile_number: str
    code: str


@handle_request_with_pydantic(RegisterRequest)
def register(req: RegisterRequest):
    existed_user: Optional[models.AuthUserTab] = models.AuthUserTab.get_or_none(username=req.username)
    if existed_user:
        log.info("[register] existed user, username=%s", req.username)
        return response(code=ReturnCode.username_existed)

    user = models.AuthUserTab.create(**{
        "username": req.username,
        "password": req.password
    })
    return response(data=model_to_dict(user))


add_route("register", register)