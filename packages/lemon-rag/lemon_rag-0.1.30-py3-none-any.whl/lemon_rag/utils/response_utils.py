import asyncio
import queue
from enum import Enum
from queue import Queue
from typing import TypeVar

import sanic.response as sanic_response
from pydantic import BaseModel

T = TypeVar("T")

timeout = 10


class ErrorCode(BaseModel):
    status: int = 200
    code: int
    message: str


class ErrorCodes:
    ok = ErrorCode(code=20000, message="OK")
    invalid_json = ErrorCode(code=40001, message="请求JSON格式错误")
    username_existed = ErrorCode(code=40002, message="用户名已存在")
    invalid_username_or_password = ErrorCode(code=40003, message="用户名或密码不正确")
    unauthorized = ErrorCode(code=40100, message="未登录", status=401)
    invalid_token = ErrorCode(code=40101, message="无效的令牌", status=401)


def response(code: ErrorCode = ErrorCodes.ok, data: T = ""):
    if isinstance(data, BaseModel):
        data = data.dict()
    return sanic_response.json({"code": code.code, "data": data, "message": code.message}, status=code.status)


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
