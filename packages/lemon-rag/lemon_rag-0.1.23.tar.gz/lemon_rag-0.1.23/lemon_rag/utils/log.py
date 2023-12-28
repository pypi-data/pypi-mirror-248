import traceback


def lemon_info(value: str):
    pass


def info(msg: str, *args):
    try:
        lemon_info(msg % args)
    except Exception as e:
        lemon_info(traceback.format_exc())
