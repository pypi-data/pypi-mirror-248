import time
import uuid
from typing import Optional

import sanic.request
from playhouse.shortcuts import model_to_dict
from pydantic import BaseModel

from lemon_rag.api.base import handle_request_with_pydantic, add_route, handle_chat_auth
from lemon_rag.core.executor_pool import submit_streaming_task
from lemon_rag.dependencies.data_access import data_access
from lemon_rag.lemon_models import models
from lemon_rag.utils import log
from lemon_rag.utils.password_match import hash_password
from lemon_rag.utils.response_utils import response, stream, ErrorCodes


class ListSessionRequest(BaseModel):
    pass


class ListSessionResponse(BaseModel):
    pass


@handle_chat_auth
@handle_request_with_pydantic(ListSessionRequest)
def list_session(req: ListSessionRequest):
    return response(data=[])


add_route("list_session", list_session)
