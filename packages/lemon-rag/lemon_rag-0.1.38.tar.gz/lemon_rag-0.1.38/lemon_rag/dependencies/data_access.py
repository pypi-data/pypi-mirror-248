import time
import uuid
from typing import Tuple

from lemon_rag.lemon_models import models
from lemon_rag.protocols.message import ChatRole


class DataAccess:
    def generate_new_auth_token(self, auth_user: models.AuthUserTab) -> models.AppAuthTokenTab:
        token = uuid.uuid4().hex
        token = models.AppAuthTokenTab.create(**{
            "token": token,
            "user": auth_user,
            "created_at": int(time.time()),
            "expire_at": int(time.time()) + 300
        })
        return token

    def get_or_create_session(self, user: models.AuthUserTab, role: ChatRole) -> Tuple[models.SessionTab, bool]:
        title = "AI助手" if role == ChatRole.assistant else "通知中心"
        return models.SessionTab.get_or_create(
            user=user,
            assistant_role=role,
            defaults={
                "created_at": int(time.time()),
                "topic": "",
                "title": title,
                "assistant_role": role
            }
        )


data_access = DataAccess()
