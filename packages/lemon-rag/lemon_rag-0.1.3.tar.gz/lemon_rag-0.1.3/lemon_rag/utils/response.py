from typing import TypeVar, Generator

from sanic.response import json, StreamingHTTPResponse

T = TypeVar("T")


def response(code: int = 200000, data: T = "", message: str = ""):
    return json({"code": code, "data": data, "message": message})


def stream(generator: Generator[T, None, None]):
    return StreamingHTTPResponse(streaming_fn=generator)
