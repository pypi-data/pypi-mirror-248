import asyncio
import queue
from enum import Enum
from queue import Queue
from typing import TypeVar

import sanic.response as sanic_response

T = TypeVar("T")


def response(code: int = 20000, data: T = "", message: str = ""):
    return sanic_response.json({"code": code, "data": data, "message": message})


timeout = 10


class ReturnCode(int, Enum):
    ok = 20000
    invalid_json = 40001
    username_existed = 40002


def stream(q: Queue):
    async def stream_from_queue(res: sanic_response.StreamingHTTPResponse):
        total_sleep = 0
        while True:
            if total_sleep >= timeout:
                raise TimeoutError()
            try:
                data = q.get_nowait()
                if data == "end":
                    break
                await res.write(data)
                print(f"writen the data {data}")
            except queue.Empty:
                await asyncio.sleep(0.5)
                total_sleep += 0.5
        print("receive end")

    return sanic_response.stream(stream_from_queue)
