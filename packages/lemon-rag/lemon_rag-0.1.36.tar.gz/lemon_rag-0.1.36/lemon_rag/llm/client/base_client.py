from typing import List

from langchain_core.messages import BaseMessage
from pydantic import BaseModel

def generate(history_messages: List[BaseMessage], metrics_name: "str") -> BaseModel:
    llm = ""
