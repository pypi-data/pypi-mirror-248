import logging
from abc import ABC

from Tea.model import TeaModel

logger = logging.getLogger("openapi")


class BaseToMapFromMapValidTeaModel(TeaModel, ABC):

    def to_map(self):

        m = dict()
        for k, v in vars(self).items():
            if k.startswith('_'):
                continue
            new_k = "".join([c.capitalize() for c in k.split('_')])
            m[new_k] = v

        return m

    def from_map(self, map=None):
        raise ValueError("Not Implemented")

    def validate(self):
        return True


class RasterParam(BaseToMapFromMapValidTeaModel):
    """
    栅格影像输入参数
    """

    def __init__(self,
                 data_id: str,
                 band_name: str = None):
        """
        平台栅格影像
        :param data_id: 影像ID
        :param band_name: 影像波段
        """
        self.data_id = data_id
        self.band_name = band_name


class MapServiceParam(BaseToMapFromMapValidTeaModel):
    """
    地图服务影像输入参数
    """

    def __init__(self,
                 data_id: str,
                 zoom_level: int):
        """
        平台OGC地图服务
        :param data_id: 地图服务ID
        :param zoom_level: 地图服务使用zoomLevel参数
        """
        self.data_id = data_id
        self.zoom_level = zoom_level
