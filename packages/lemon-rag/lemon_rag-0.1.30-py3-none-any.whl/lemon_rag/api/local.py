import threading
import uuid
from contextlib import contextmanager
from typing import Optional

from lemon_rag.lemon_models.models import AuthUserTab

request_context = threading.local()


def get_rid() -> str:
    if hasattr(request_context, "rid"):
        return request_context.rid
    return "not-set"


def get_user() -> Optional[AuthUserTab]:
    if hasattr(request_context, "user"):
        return request_context.user
    return None


@contextmanager
def with_rid():
    try:
        rid = uuid.uuid4().hex
        request_context.rid = rid
        yield rid
    finally:
        del request_context.rid


@contextmanager
def with_auth(auth_user: AuthUserTab):
    try:
        request_context.user = auth_user
        yield
    finally:
        del request_context.user
