import json
import logging

from oss2 import StsAuth, Bucket

from aiearth.openapi.client._utils import get_sts_token, publish_vector
from aiearth.openapi.enums import DataType
from aiearth.openapi.models import PublishLocalTiffRequest, PublishLocalTiffResponse, BasePublishLocalResponseBody, \
    PublishLocalImgRequest, PublishLocalImgResponse, PublishLocalImgIgeRequest, PublishLocalImgIgeResponse, \
    PublishLocalTiffRpcRequest, PublishLocalTiffRpcResponse, PublishLocalTiffRpbRequest, PublishLocalTiffRpbResponse, \
    PublishLocalTiffTfwRequest, PublishLocalTiffTfwResponse, PublishLocalShapefileRequest, PublishLocalShapefileResponse
from aiearth.openapi.oss import StsToken
from aiearth.openapi.client._publisher import TiffPublisher, ImgPublisher, ImgIgePublisher, TiffRpcPublisher, TiffRpbPublisher, \
    TiffTfwPublisher
from aiearth.openapi.utils import TqdmUpTo

logger = logging.getLogger("openapi")


class ImagePublisherClient:
    def publish_local_tiff(self, request: PublishLocalTiffRequest) -> PublishLocalTiffResponse:
        tiff_publisher: TiffPublisher = TiffPublisher(request.local_file_path, request.name, request.acquisition_date)
        resp = tiff_publisher.publish()
        body = BasePublishLocalResponseBody(resp['dataId'], resp['name'])
        return PublishLocalTiffResponse({}, 200, body)

    def publish_local_img(self, request: PublishLocalImgRequest) -> PublishLocalImgResponse:
        img_publisher = ImgPublisher(request.local_file_path, request.name, request.acquisition_date)
        resp = img_publisher.publish()
        body = BasePublishLocalResponseBody(resp['dataId'], resp['name'])
        return PublishLocalImgResponse({}, 200, body)

    def publish_local_img_ige(self, request: PublishLocalImgIgeRequest) -> PublishLocalImgIgeResponse:
        img_ige_publisher = ImgIgePublisher(request.main_file_path, request.attach_file_path, request.name,
                                            request.acquisition_date)
        resp = img_ige_publisher.publish()
        body = BasePublishLocalResponseBody(resp['dataId'], resp['name'])
        return PublishLocalImgIgeResponse({}, 200, body)

    def publish_local_tiff_rpc(self, request: PublishLocalTiffRpcRequest) -> PublishLocalTiffRpcResponse:
        tiff_rpc_publisher = TiffRpcPublisher(request.main_file_path, request.attach_file_path, request.name,
                                              request.acquisition_date)
        resp = tiff_rpc_publisher.publish()
        body = BasePublishLocalResponseBody(resp['dataId'], resp['name'])
        return PublishLocalTiffRpcResponse({}, 200, body)

    def publish_local_tiff_rpb(self, request: PublishLocalTiffRpbRequest) -> PublishLocalTiffRpbResponse:
        tiff_rpb_publisher = TiffRpbPublisher(request.main_file_path, request.attach_file_path, request.name,
                                              request.acquisition_date)
        resp = tiff_rpb_publisher.publish()
        body = BasePublishLocalResponseBody(resp['dataId'], resp['name'])
        return PublishLocalTiffRpbResponse({}, 200, body)

    def publish_local_tiff_tfw(self, request: PublishLocalTiffTfwRequest) -> PublishLocalTiffTfwResponse:
        tiff_tfw_publisher = TiffTfwPublisher(request.main_file_path, request.attach_file_path, request.name,
                                              request.acquisition_date)
        resp = tiff_tfw_publisher.publish()
        body = BasePublishLocalResponseBody(resp['dataId'], resp['name'])
        return PublishLocalTiffTfwResponse({}, 200, body)

    def publish_local_shapefile(self, request: PublishLocalShapefileRequest) -> PublishLocalShapefileResponse:
        if request.name is None or len(request.name.strip()) == 0:
            raise ValueError(f"不合法的影像名称 {request.name}")

        resp = get_sts_token('zip', data_type=DataType.VECTOR)
        logger.debug(f"get_sts_token for zip get {resp}")
        sts_token = StsToken(json.loads(resp)['module'])

        auth = StsAuth(sts_token.access_key_id, sts_token.access_key_secret, sts_token.security_token)
        bucket = Bucket(auth, endpoint=sts_token.endpoint, bucket_name=sts_token.bucket)
        logger.debug(f"uploading {request.local_file_path} to {sts_token.bucket}/{sts_token.file_key}")
        with TqdmUpTo(desc=f"Uploading {request.local_file_path}") as t:
            bucket.put_object_from_file(sts_token.file_key, request.local_file_path, progress_callback=t.update_to)
            t.total = t.n

        resp = publish_vector(request.name,
                                oss_file_key=f"oss://{sts_token.bucket}/{sts_token.file_key}")
        module = json.loads(resp)['module']
        vector_id = module[0]['vectorId']
        name = module[0]['vectorName']
        return PublishLocalShapefileResponse({}, 200, BasePublishLocalResponseBody(vector_id, name))