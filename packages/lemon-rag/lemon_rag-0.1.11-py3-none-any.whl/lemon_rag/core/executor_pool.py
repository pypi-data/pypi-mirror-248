import queue
from concurrent.futures import ThreadPoolExecutor
from typing import Generator

streaming_pool = ThreadPoolExecutor(max_workers=16)


def submit_streaming_task(generator: Generator[str, None, None]) -> queue.Queue:
    q = queue.Queue(maxsize=128)

    def inner_task():
        for value in generator:
            q.put(value)

    streaming_pool.submit(inner_task)
    return q
