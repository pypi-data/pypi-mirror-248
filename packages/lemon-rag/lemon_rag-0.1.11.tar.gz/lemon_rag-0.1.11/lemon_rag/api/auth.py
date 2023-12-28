import time

import sanic.request

from lemon_rag.core.executor_pool import submit_streaming_task
from lemon_rag.utils.response_utils import response, stream


def hello_world(request: sanic.request.Request):
    return response(message="Hello world!")


def hello_stream(request: sanic.request.Request):
    def generator():
        for line in ["aaaaa", "bbbbb", "ccccc", "ddddd"]:
            yield line
            time.sleep(1)
    queue = submit_streaming_task(generator())

    return stream(queue)
