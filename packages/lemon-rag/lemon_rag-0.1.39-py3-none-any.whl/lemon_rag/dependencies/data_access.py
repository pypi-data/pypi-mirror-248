import time
import uuid
from enum import Enum
from typing import Tuple

from lemon_rag.lemon_runtime import models
from lemon_rag.protocols.message import ChatRole


class KnowledgeBasePermission(int, Enum):
    read = 1
    write = 1 << 1
    read_write = read & write


class DataAccess:
    def generate_new_auth_token(self, auth_user: models.AuthUserTab) -> models.AppAuthTokenTab:
        token = uuid.uuid4().hex
        token = models.AppAuthTokenTab.create(**{
            "token": token,
            "user": auth_user,
            "created_at": int(time.time()),
            "expire_at": int(time.time()) + 60 * 60 * 24 * 100
        })
        return token

    def get_or_create_session(self, user: models.AuthUserTab, role: ChatRole) -> Tuple[models.SessionTab, bool]:
        title = "AI助手" if role == ChatRole.assistant else "通知中心"
        session, create = models.SessionTab.get_or_create(
            user=user,
            assistant_role=role,
            defaults={
                "created_at": int(time.time()),
                "topic": "",
                "title": title,
                "assistant_role": role,
                "last_msg_id": 0,
                "last_msg_ts": int(time.time())
            }
        )
        if create:
            models.SyncHistoryTab.create(**{
                "session": session,
                "last_read_id": 0,
                "last_read_ts": int(time.time())
            })
        return session

    def read_message(self, session: models.SessionTab, read_id: int) -> int:
        return models.SyncHistoryTab.update(
            **{"last_read_id": read_id, "last_read_ts": int(time.time())}
        ).where(models.SyncHistoryTab.session == session).execute()

    def init_account(self, user: models.AuthUserTab):
        self.create_knowledge_base(
            user, "默认知识库", 5
        )

    def create_knowledge_base(self, user: models.AuthUserTab, name: str, max_files: int):
        kb = models.KnowledgeBaseTab.create(**{
            "name": name,
            "owner": user,
            "max_files": max_files
        })
        models.KnowledgeBaseAccessTab.create(
            **{
                "permission": KnowledgeBasePermission.read_write,
                "create_at": int(time.time()),
                "user": user,
                "knowledge_base": kb,
                "creator": user
            },
        )
        return kb


data_access = DataAccess()
