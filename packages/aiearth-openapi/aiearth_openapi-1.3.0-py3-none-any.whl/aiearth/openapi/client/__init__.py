import logging

from aiearth.core import g_var
from alibabacloud_aiearth_engine20220609.client import Client

from aiearth.openapi.client.aieseg_client import AiesegClient
from aiearth.openapi.client.imagepublisher_client import ImagePublisherClient

logger = logging.getLogger("openapi")


class ExtClient(Client, AiesegClient, ImagePublisherClient):
    pass
