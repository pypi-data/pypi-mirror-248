from pydantic import BaseModel

from lemon_rag.api.base import handle_request_with_pydantic, add_route, handle_chat_auth
from lemon_rag.utils.response_utils import response


class ListSessionRequest(BaseModel):
    pass


class ListSessionResponse(BaseModel):
    pass


@handle_chat_auth
@handle_request_with_pydantic(ListSessionRequest)
def list_session(req: ListSessionRequest):
    return response(data=[])


add_route("list_session", list_session)
