from typing import List, Optional

from playhouse.shortcuts import model_to_dict
from pydantic import BaseModel

from lemon_rag.api.base import handle_request_with_pydantic, add_route, handle_chat_auth
from lemon_rag.api.local import get_user
from lemon_rag.dependencies.data_access import data_access
from lemon_rag.lemon_runtime import models
from lemon_rag.protocols.message import ChatRole, Session
from lemon_rag.utils.response_utils import response


class ListSessionRequest(BaseModel):
    version: int


class ListSessionResponse(BaseModel):
    up_to_date: bool = False
    sessions: Optional[List[Session]] = None


@handle_chat_auth
@handle_request_with_pydantic(ListSessionRequest)
def list_session(req: ListSessionRequest):
    assistant_session, _ = data_access.get_or_create_session(get_user(), ChatRole.assistant)
    notification_session, _ = data_access.get_or_create_session(get_user(), ChatRole.notification_center)
    return response(data=ListSessionResponse(sessions=[
        Session(**model_to_dict(assistant_session)),
        Session(**model_to_dict(notification_session))
    ]))


class GetNotificationCountRequest(BaseModel):
    version: int


class GetNotificationCountResponse(BaseModel):
    version: int
    unread_count: int


@handle_chat_auth
@handle_request_with_pydantic(GetNotificationCountRequest)
def get_notification_count(req: GetNotificationCountRequest):
    notification_session, _ = data_access.get_or_create_session(get_user(), ChatRole.notification_center)
    sync_history: models.SyncHistoryTab = notification_session.sync_history.get()
    return response(data=GetNotificationCountResponse(
        version=notification_session.version,
        unread_count=(notification_session.last_msg_id or 0) - (sync_history.last_read_id or 0)
    ))


class ReadNotificationsRequest(BaseModel):
    msg_id: int


@handle_chat_auth
@handle_request_with_pydantic(ReadNotificationsRequest)
def read_notifications(req: ReadNotificationsRequest):
    notification_session, _ = data_access.get_or_create_session(get_user(), ChatRole.notification_center)
    data_access.read_message(notification_session, msg_id=req.msg_id)
    return response()


class CreateKnowledgeBaseRequest(BaseModel):
    name: str


@handle_chat_auth
@handle_request_with_pydantic(CreateKnowledgeBaseRequest)
def create_knowledge_base(req: CreateKnowledgeBaseRequest):
    data_access.create_knowledge_base()


add_route("list_session", list_session)
