from lemon_rag.lemon_models import models as m


def insert_default_admin_account():
    m.AuthUserTab.create(
        **{
            "username": "admin",
            "password": "admin",
            "nickname": "admin",
            "avatar": "",
        }
    )
