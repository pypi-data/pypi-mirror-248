import json
import logging
import os
from datetime import datetime
from typing import Union, List, Tuple
from urllib import parse

import imagesize
from aiearth.core.client import Endpoints
from aiearth.core.client.client import BaseClient
from numpy import ndarray
from oss2 import StsAuth, Bucket

from aiearth import core
from aiearth.openapi.enums import DataType, RasterFileType
from aiearth.openapi.oss import StsToken
from aiearth.openapi.utils import TqdmUpTo

logger = logging.getLogger("openapi")


def get_host() -> str:
    host = Endpoints.HOST
    data_host = os.getenv("DATA_CLIENT_HOST")
    return data_host if (data_host is not None and len(data_host) > 0) else host


def get_sts_token(file_ext: str, data_type: DataType, prev_file_name: str = None):
    url = get_host() + f"/mariana/openapi/oss/getStsToken?client=aiearthopenapi&data_type={data_type.name}&file_ext={file_ext}"
    if prev_file_name:
        url = url + f"&prev_file_name={parse.quote(prev_file_name)}"
    resp = BaseClient.get(url, {})
    return resp.content.decode(encoding='utf-8')


def get_sts_object(file_ext: str, data_type: DataType, prev_file_name: str = None):
    resp = get_sts_token(file_ext, data_type, prev_file_name)
    return StsToken(json.loads(resp)['module'])


# def __get_aieseg_sts_token__(file_ext: str):
#     url = __get_host__() + f"/mariana/openapi/oss/getAiesegMaskStsToken?bgPicExt={file_ext}"
#     resp = BaseClient.get(url, {})
#     return resp.content.decode(encoding='utf-8')


def publish_vector(name: str,
                   oss_file_key: str):
    url = f'{get_host()}/mariana/openapi/shape/v2/batchPublish?client=aiearthopenapi'
    resp = BaseClient.post(url, {}, data=[{
        'name': name,
        'fileUrl': oss_file_key
    }])
    return resp.content.decode(encoding='utf-8')


def publish_raster(name: str,
                   file_type: RasterFileType,
                   attach_file_type: RasterFileType = None,
                   oss_file_key: str = None,
                   attach_oss_file_key: str = None,
                   acquisition_date: int = None,
                   download_url: str = None,
                   attach_download_url: str = None):
    url = get_host() + "/mariana/openapi/tiff/v2/batchPublish?client=aiearthopenapi"
    resp = BaseClient.post(url, {}, data=[{
        "file_type": file_type.value,
        "attach_file_type": attach_file_type.value if attach_file_type else None,
        "tiff_date": acquisition_date,
        "name": name,
        "file_url": oss_file_key,
        "attach_file_url": attach_oss_file_key,
        "download_url": download_url,
        "attach_download_url": attach_download_url
    }])
    return resp.content.decode(encoding="utf-8")


def get_token() -> str:
    return core.g_var.get_var(core.g_var.GVarKey.Authenticate.TOKEN) or None


def do_oss_upload(sts_token: StsToken, local_file_path: str):
    auth = StsAuth(sts_token.access_key_id, sts_token.access_key_secret, sts_token.security_token)
    bucket = Bucket(auth, endpoint=sts_token.endpoint, bucket_name=sts_token.bucket)
    logger.debug(f"uploading {local_file_path} to {sts_token.bucket}/{sts_token.file_key}")
    with TqdmUpTo(desc=f"Uploading {local_file_path}") as t:
        bucket.put_object_from_file(sts_token.file_key, local_file_path, progress_callback=t.update_to)
        t.total = t.n


def do_oss_upload_from_bytes(sts_token: StsToken, local_bytes: bytes):
    auth = StsAuth(sts_token.access_key_id, sts_token.access_key_secret, sts_token.security_token)
    bucket = Bucket(auth, endpoint=sts_token.endpoint, bucket_name=sts_token.bucket)
    logger.debug(f"uploading bytes to {sts_token.bucket}/{sts_token.file_key}")
    with TqdmUpTo(desc=f"Uploading bytes") as t:
        bucket.put_object(sts_token.file_key, local_bytes)
        t.total = t.n


_width_limit = 500
_height_limit = 2000


def check_bg_mask(img: Union[ndarray, str]):
    if isinstance(img, str):
        width, height = imagesize.get(img)
    elif isinstance(img, ndarray):
        height, width = img.shape[0], img.shape[1]
    else:
        raise ValueError(f"参数img类型{type(img)}不支持")
    if not all((_width_limit <= width <= _height_limit, _width_limit <= height <= _height_limit)):
        raise ValueError(f"仅支持宽高都在[{_width_limit}, {_height_limit}]之间的图形提示")


def valid_bbox(bbox):
    if not isinstance(bbox, (List, Tuple)) or len(bbox) != 4:
        raise ValueError(f"Bbox格式为 [1, 2, 3, 4]")
    if bbox[0] >= bbox[2] or bbox[1] >= bbox[3]:
        raise ValueError(f"Bbox值错误，需要表示左上，右下两个点, 比如[1,2,3,4]")


def milli_sec_2_datetime(milli_sec: Union[str, int]):
    return datetime.fromtimestamp(int(milli_sec) / 1000)
