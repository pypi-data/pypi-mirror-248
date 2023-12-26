import json
import logging
import os
from abc import abstractmethod, ABC
from datetime import datetime

from oss2 import Bucket, StsAuth

from aiearth.openapi.client._utils import get_sts_token, publish_raster
from aiearth.openapi.enums import DataType, RasterFileType, AttachRasterFileType
from aiearth.openapi.oss import StsToken
from aiearth.openapi.utils import TqdmUpTo

logger = logging.getLogger("openapi")


class BaseDoubleFilePublisher(ABC):

    def __init__(self, main_file_path: str, attach_file_path: str,
                 name: str, acquisition_date: str = None):
        self.__main_file_path = main_file_path
        self.__attach_file_path = attach_file_path
        if name is None or len(name.strip()) == 0:
            raise ValueError(f"不合法的影像名称 {name}")
        self.__name = name
        self.__acquisition_date_dt = datetime.strptime(acquisition_date, "%Y%m%d") if acquisition_date else None

    def get_sts_token(self):
        resp = get_sts_token(self.exts()[0], data_type=DataType.RASTER)
        logger.debug(f"get_sts_token for {self.exts()[0]} get {resp}")
        self.__sts_token = StsToken(json.loads(resp)['module'])

        prev_file_name = os.path.basename(self.__sts_token.file_key)
        resp_ige = get_sts_token(self.exts()[1], data_type=DataType.RASTER,
                                 prev_file_name=prev_file_name)
        logger.debug(f"get_sts_token for {self.exts()[1]} with {self.__sts_token.file_key} get {resp_ige}")
        self.__sts_token_attach = StsToken(json.loads(resp_ige)['module'])

    @abstractmethod
    def exts(self):
        pass

    def upload_file_to_oss(self):
        auth = StsAuth(self.__sts_token.access_key_id, self.__sts_token.access_key_secret,
                       self.__sts_token.security_token)
        bucket = Bucket(auth, endpoint=self.__sts_token.endpoint, bucket_name=self.__sts_token.bucket)

        # upload main file
        logger.debug(f"uploading {self.__main_file_path} to {self.__sts_token.endpoint} {self.__sts_token.bucket}/{self.__sts_token.file_key}")
        with TqdmUpTo(desc=f"Uploading {self.__main_file_path}") as t:
            bucket.put_object_from_file(self.__sts_token.file_key, self.__main_file_path,
                                        progress_callback=t.update_to)
            t.total = t.n

        # upload attach file
        auth = StsAuth(self.__sts_token_attach.access_key_id, self.__sts_token_attach.access_key_secret,
                       self.__sts_token_attach.security_token)
        bucket = Bucket(auth, endpoint=self.__sts_token_attach.endpoint, bucket_name=self.__sts_token_attach.bucket)
        logger.debug(
            f"uploading {self.__attach_file_path} to {self.__sts_token_attach.endpoint} {self.__sts_token_attach.bucket}/{self.__sts_token_attach.file_key}")
        with TqdmUpTo(desc=f"Uploading {self.__attach_file_path}") as t:
            bucket.put_object_from_file(self.__sts_token_attach.file_key, self.__attach_file_path,
                                        progress_callback=t.update_to)
            t.total = t.n

    def publish_file(self):
        acquisition_date = int(self.__acquisition_date_dt.timestamp() * 1000) if self.__acquisition_date_dt else None
        resp = publish_raster(self.__name,
                              file_type=self.file_types()[0],
                              attach_file_type=self.file_types()[1],
                              oss_file_key=f"oss://{self.__sts_token.bucket}/{self.__sts_token.file_key}",
                              attach_oss_file_key=f'oss://{self.__sts_token_attach.bucket}/{self.__sts_token_attach.file_key}',
                              acquisition_date=acquisition_date)
        module: dict = json.loads(resp)['module']
        return [{'dataId': a['stacId'], 'name': a['tiffName']} for a in module][0]

    @abstractmethod
    def file_types(self):
        pass

    def publish(self):
        self.get_sts_token()
        self.upload_file_to_oss()
        return self.publish_file()


class TiffTfwPublisher(BaseDoubleFilePublisher):

    def exts(self):
        return "tif", "tfw"

    def file_types(self):
        return RasterFileType.TIFF, AttachRasterFileType.TFW


class TiffRpcPublisher(BaseDoubleFilePublisher):
    def exts(self):
        return "tif", "_rpc.txt"

    def file_types(self):
        return RasterFileType.TIFF, AttachRasterFileType.RPC


class TiffRpbPublisher(BaseDoubleFilePublisher):
    def exts(self):
        return 'tif', 'rpb'

    def file_types(self):
        return RasterFileType.TIFF, AttachRasterFileType.RPB


class ImgIgePublisher(BaseDoubleFilePublisher):

    def exts(self):
        return 'img', 'ige'

    def file_types(self):
        return RasterFileType.IMG, AttachRasterFileType.IGE


class BaseSingleFilePublisher(ABC):

    def __init__(self,
                 local_file_path: str,
                 name: str,
                 acquisition_date: str = None):
        """
        EN: publish local file to AI Earth;
        1. upload local file to oss
        2. publish this file
        :param local_file_path: accepts tif / img file 接收 tif / img 影像
        :param name: the published resource name 发布的影像资源的名称
        :param acquisition_date: the date (in %y%m%d format) this image acquired 该影响的获取时间
        """
        self.__local_file_path__ = local_file_path
        if name is None or len(name.strip()) == 0:
            raise ValueError(f"不合法的影像名称 {name}")
        self.__raster_name__ = name

        # parse acquisition date
        self.__acquisition_date_dt = datetime.strptime(acquisition_date, '%Y%m%d') if acquisition_date else None

    def get_sts_token(self):
        resp = get_sts_token(self.file_ext(), data_type=DataType.RASTER)
        logger.debug(f"get_sts_token: {resp}")
        self.__sts_token = StsToken(json.loads(resp)['module'])

    def upload_file_to_oss(self):
        auth = StsAuth(self.__sts_token.access_key_id, self.__sts_token.access_key_secret,
                       self.__sts_token.security_token)
        bucket = Bucket(auth, endpoint=self.__sts_token.endpoint, bucket_name=self.__sts_token.bucket)

        logger.debug(f"uploading {self.__local_file_path__} to {self.__sts_token.endpoint} {self.__sts_token.bucket}/{self.__sts_token.file_key}")

        with TqdmUpTo(desc=f"Uploading {self.__local_file_path__}") as t:
            bucket.put_object_from_file(self.__sts_token.file_key, self.__local_file_path__,
                                        progress_callback=t.update_to)
            t.total = t.n

    def publish_file(self):
        acquisition_date = int(self.__acquisition_date_dt.timestamp() * 1000) if self.__acquisition_date_dt else None
        resp = publish_raster(self.__raster_name__, file_type=self.file_type(),
                              oss_file_key=f"oss://{self.__sts_token.bucket}/{self.__sts_token.file_key}",
                              acquisition_date=acquisition_date)
        module: dict = json.loads(resp)['module']
        return [{'dataId': a['stacId'], 'name': a['tiffName']} for a in module][0]

    def publish(self):
        self.get_sts_token()
        self.upload_file_to_oss()
        return self.publish_file()

    @abstractmethod
    def file_ext(self):
        pass

    @abstractmethod
    def file_type(self):
        pass


class ImgPublisher(BaseSingleFilePublisher):

    def file_ext(self):
        return "img"

    def file_type(self):
        return RasterFileType.IMG


class TiffPublisher(BaseSingleFilePublisher):

    def file_ext(self):
        return "tif"

    def file_type(self):
        return RasterFileType.TIFF
