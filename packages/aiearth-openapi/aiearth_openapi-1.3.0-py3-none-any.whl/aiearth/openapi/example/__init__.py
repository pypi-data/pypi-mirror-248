import logging
import urllib.parse

from aiearth.core.client.client import BaseClient

from aiearth.openapi.client._utils import get_host

logger = logging.getLogger("openapi")


def load_image_example(key):
    url = get_host() + f"/mariana/openapi/mariana/static/files?key={urllib.parse.quote(key)}"
    resp = BaseClient.get(url, {})
    if resp.status_code != 200:
        raise ValueError(
            f"请求example数据失败, status code {resp.status_code}, content: {resp.content.decode(encoding='utf-8')}")

    return resp.content.decode(encoding='utf-8')
