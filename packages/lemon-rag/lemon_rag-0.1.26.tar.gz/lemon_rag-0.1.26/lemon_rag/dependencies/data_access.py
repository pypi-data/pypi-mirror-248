import time
import uuid

from lemon_rag.lemon_models import models


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


data_access = DataAccess()
