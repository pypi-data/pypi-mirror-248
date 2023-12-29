from typing import List

from playhouse.shortcuts import model_to_dict
from pydantic import BaseModel

from lemon_rag.api.base import handle_request_with_pydantic, add_route, handle_chat_auth
from lemon_rag.api.local import get_user
from lemon_rag.dependencies.data_access import data_access
from lemon_rag.protocols.message import ChatRole, Session
from lemon_rag.utils.response_utils import response


class ListSessionRequest(BaseModel):
    version: int


class ListSessionResponse(BaseModel):
    sessions: List[Session]


@handle_chat_auth
@handle_request_with_pydantic(ListSessionRequest)
def list_session(req: ListSessionRequest):
    assistant_session, _ = data_access.get_or_create_session(get_user(), ChatRole.assistant)
    notification_session, _ = data_access.get_or_create_session(get_user(), ChatRole.notification_center)
    return response(data=ListSessionResponse(sessions=[
        Session(**model_to_dict(assistant_session)),
        Session(**model_to_dict(notification_session))
    ]))


add_route("list_session", list_session)
