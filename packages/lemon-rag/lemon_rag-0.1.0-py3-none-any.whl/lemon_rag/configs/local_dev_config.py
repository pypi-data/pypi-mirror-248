import os.path
from typing import Optional

from pydantic import BaseModel


class LemonClientConfig(BaseModel):
    base_url: str
    app_uuid: str
    module_uuid: str
    username: str
    password: str


class LocalDEVConfig(BaseModel):
    lemon: LemonClientConfig


config: Optional[LocalDEVConfig] = None
dev_config_path = os.path.join(os.path.dirname(__file__), "local_dev_config.json")
if os.path.exists(dev_config_path):
    config = LocalDEVConfig.parse_file(dev_config_path)
