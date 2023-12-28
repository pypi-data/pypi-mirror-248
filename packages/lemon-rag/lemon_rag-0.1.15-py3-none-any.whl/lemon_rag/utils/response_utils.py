import asyncio
import queue
from queue import Queue
from typing import TypeVar

import sanic.response as sanic_response


T = TypeVar("T")


def response(code: int = 200000, data: T = "", message: str = ""):
    return sanic_response.json({"code": code, "data": data, "message": message})


timeout = 200


def stream(q: Queue):
    async def stream_from_queue(res: sanic_response.StreamingHTTPResponse):
        total_sleep = 0
        while True:
            if total_sleep >= timeout:
                raise TimeoutError()
            try:
                data = q.get_nowait()
                if data == "end":
                    return
                await res.write(data)
            except queue.Empty:
                await asyncio.sleep(0.5)
                total_sleep += 0.5

    return sanic_response.StreamingHTTPResponse(stream_from_queue)
