import sys

import requests

from lemon_rag.configs.local_dev_config import config


def api_update_current_package(package: str, v: str):
    res = requests.post(
        f"https://lemon.lemonstudio.tech:{8443}/{config.lemon.app_uuid}/{config.lemon.tenant_uuid}/restful/v1/update_module",
        {"name": package, "version": v, "registry": "https://pypi.python.org/simple/"}

    )


if __name__ == '__main__':
    name, version = sys.argv[1].split(" ")
    api_update_current_package(name, version)
