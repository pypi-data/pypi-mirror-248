import time

import sanic.request

from lemon_rag.utils.response import response, stream


def hello_world(request: sanic.request.Request):
    return response(message="Hello world!")


def hello_stream(request: sanic.request.Request):
    def generator():
        for line in ["aaaaa", "bbbbb", "ccccc", "ddddd"]:
            yield line
            time.sleep(1)

    return stream(generator())
