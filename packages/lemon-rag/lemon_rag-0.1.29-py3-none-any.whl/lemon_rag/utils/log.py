import traceback

from lemon_rag.api.local import get_rid, get_user


def lemon_info(value: str):
    pass


def info(msg: str, *args):
    suffix = f" rid={get_rid()} user_id={get_user()}"
    try:
        lemon_info((msg + suffix) % args)
    except Exception as e:
        lemon_info(traceback.format_exc())
