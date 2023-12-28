import asyncio
import queue
import threading
import time
from queue import Queue
from typing import TypeVar, Generator, AsyncGenerator

from sanic.response import json, StreamingHTTPResponse, HTTPResponse

T = TypeVar("T")


def response(code: int = 200000, data: T = "", message: str = ""):
    return json({"code": code, "data": data, "message": message})


class CustomStreamingHTTPResponse(StreamingHTTPResponse, HTTPResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


timeout = 200


def stream(q: Queue):
    async def stream_from_queue(res: StreamingHTTPResponse):
        total_sleep = 0
        while True:
            if total_sleep >= timeout:
                raise TimeoutError()
            try:
                data = await q.get_nowait()
                if data == "end":
                    return
                await res.write(data)
            except queue.Empty:
                await asyncio.sleep(0.5)
                total_sleep += 0.5

    return CustomStreamingHTTPResponse(stream_from_queue)
