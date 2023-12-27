import sys

import requests

from lemon_rag.configs.local_dev_config import config


def api_update_current_package(package: str, v: str):
    url = f"https://lemon.lemonstudio.tech:8443/{config.lemon.app_uuid}test/{config.lemon.tenant_uuid}/restful/v1/update_module"
    print(url)
    res = requests.post(
        url,
        json={"name": package, "version": v, "registry": "https://pypi.python.org/simple/"}

    )
    res.raise_for_status()
    print(res.json().get("output"))


if __name__ == '__main__':
    name, version = sys.argv[1:]
    api_update_current_package(name, version)
