import base64
import json
import logging
import os
import tempfile
from operator import xor
from os.path import splitext
from typing import List, Tuple
from urllib import parse

import cv2
import numpy as np
from aiearth.core.client.client import BaseClient
from alibabacloud_aiearth_engine20220609.models import CreateAIJobResponse, CreateAIJobResponseBodyJobs, \
    CreateAIJobResponseBody
from numpy import ndarray

from aiearth.openapi.client._utils import get_sts_object, do_oss_upload, get_host, check_bg_mask, valid_bbox, \
    do_oss_upload_from_bytes
from aiearth.openapi.enums import DataType, AiesegJobType
from aiearth.openapi.models import DeleteAiesegVisualPromptRequest, DeleteAiesegVisualPromptResponse, \
    UpdateAiesegVisualPromptRequest, PublishOrUpdateAiesegVisualPromptResponse, DeleteAiesegVisualPromptResponseBody, \
    PublishOrUpdateAiesegVisualPromptResponseBody, AiesegVisualPrompt, GetAiesegVisualPromptRequest, \
    GetAiesegVisualPromptResponse, GetAiesegVisualPromptResponseBody, PublishAiesegVisualPromptRequest, \
    GenerateAieSegVisualPromptRequest, GenerateAieSegVisualPromptResponse, GenerateAieSegVisualPromptResponseBody, \
    RasterParam, MapServiceParam, CreateAiesegJobRequest
from aiearth.openapi.oss import StsToken

logger = logging.getLogger("openapi")


class AiesegClient:

    def create_aieseg_job(self, request: CreateAiesegJobRequest) -> CreateAIJobResponse:
        """
        创建aieseg任务
        :param request: 创建任务参数 `~CreateAiesegJobRequest`
        :return: 返回任务的ID
        """

        url = get_host() + f"/mariana/openapi/job/ai/submit"

        src = None
        if isinstance(request.input, RasterParam):
            src = {
                "dataId": request.input.data_id,
                "type": DataType.RASTER.name,
                "band_no": request.input.band_name
            }
        elif isinstance(request.input, MapServiceParam):
            src = {
                "dataId": request.input.data_id,
                "type": DataType.MAP_SERVICE.name,
                "mapServiceZoomLevel": request.input.zoom_level
            }

        if request.aieseg_job_type == AiesegJobType.AIE_SEG_PROMPT and request.pixel_threshold is None:
            request.pixel_threshold = 50

        data = {
            "project_id": request.project_id,
            "job_name": request.job_name,
            "app": f"{request.aieseg_job_type.value}",
            "tiff_ids": [
                {
                    "idx": 1,
                    "src": src
                }
            ],
            "ratio": request.confidence,
            "area_ratio": request.pixel_threshold,
            "referShapeDataId": request.filter_shape_data_id,
            "refer_shape_wkt": request.filter_shape_wkt,
            "extras": {
                "mask_prompt_id": request.visual_prompt_id
            }
        }

        if request.text_prompt:
            data['extras']['text_prompt'] = {
                "text_prompt_list": request.text_prompt
            }

        logger.debug(f"提交AIESEG任务 url: {url}, body: {data}")
        resp = BaseClient.post(url, {}, data)
        if resp.status_code != 200:
            raise ValueError(f"提交AIESEG任务服务出错: {resp.status_code} {resp.content.decode(encoding='utf-8')}")
        else:
            resp_content = resp.content.decode('utf-8')
            resp_object = json.loads(resp_content)
            success = resp_object.get('success', False)
            if not success:
                raise ValueError(f"提交AIESEG任务服务出错: {resp_content}")
            module = resp_object.get("module")

            app = module['app']
            success = module.get('success', list())
            failed = module.get('failed', list())

            jobs: List[CreateAIJobResponseBodyJobs] = list()
            for s in success:
                job = CreateAIJobResponseBodyJobs(job_id=s['job_id'], name=s['job_name'], success=True)
                jobs.append(job)
            for f in failed:
                job = CreateAIJobResponseBodyJobs(job_id=f['job_id'], name=f['job_name'], success=False)
                jobs.append(job)
            resp_body = CreateAIJobResponseBody(app=app, jobs=jobs, project_id=request.project_id, request_id=None)
            return CreateAIJobResponse(headers={}, status_code=200, body=resp_body)

    def delete_aieseg_visual_prompt(self, request: DeleteAiesegVisualPromptRequest) -> DeleteAiesegVisualPromptResponse:
        """
        删除平台上管理的一个图形提示
        :param request: 删除的参数 `~DeleteAiesegVisualPromptRequest`
        :return: 图形提示是否删除成功
        """
        if len(request.prompt_id.strip()) < 1:
            raise ValueError("不合法的参数 prompt_id")

        logger.info(f"删除图形提示 {request.prompt_id}")
        # call update
        url = get_host() + f"/mariana/openapi/mariana/aieseg/prompts?promptId={request.prompt_id}"
        resp = BaseClient.delete(url, {})
        if resp.status_code != 200:
            raise ValueError(f"删除图形提示服务出错: {resp.status_code} {resp.content.decode(encoding='utf-8')}")
        else:
            resp_content = resp.content.decode('utf-8')
            resp_object = json.loads(resp_content)
            success = resp_object.get('success', False)
            if not success:
                raise ValueError(f"删除图形提示服务出错: {resp_content}")
            module = resp_object.get("module")

            return DeleteAiesegVisualPromptResponse({}, 200, DeleteAiesegVisualPromptResponseBody(module))

    def update_aieseg_visual_prompt(self, request: UpdateAiesegVisualPromptRequest) \
            -> PublishOrUpdateAiesegVisualPromptResponse:
        """
        更新图形提示的内容
        :param request: 更新参数 `~UpdateAiesegVisualPromptRequest`
        :return: 更新后的图形提示
        """

        bg_sts = None
        mask_sts = None
        if request.bg_image is not None:
            check_bg_mask(request.bg_image)
            # save bg image file to local
            bg_local_file_path = request.bg_image
            if isinstance(request.bg_image, ndarray):
                bg_local_file_path = tempfile.NamedTemporaryFile(suffix=".png").name
                cv2.imwrite(bg_local_file_path, request.bg_image)
            # get bgImgSts
            bg_sts: StsToken = get_sts_object(splitext(bg_local_file_path)[1][1:], DataType.AIESEG)
            do_oss_upload(bg_sts, bg_local_file_path)
        if request.mask_image is not None:
            check_bg_mask(request.mask_image)
            # save mask file to local
            mask_local_file_path = request.mask_image
            if isinstance(request.mask_image, ndarray):
                mask_local_file_path = tempfile.NamedTemporaryFile(suffix=".png").name
                cv2.imwrite(mask_local_file_path, request.mask_image)
            mask_sts: StsToken = get_sts_object("png", DataType.AIESEG)
            do_oss_upload(mask_sts, mask_local_file_path)

        # call update
        url = get_host() + f"/mariana/openapi/mariana/aieseg/prompts"
        data = {
            "promptId": request.prompt_id
        }
        if request.name:
            data['name'] = request.name
        if bg_sts:
            data['backgroundFileUri'] = f"oss://{bg_sts.bucket}/{bg_sts.file_key}"
        if mask_sts:
            data['maskFileUri'] = f"oss://{mask_sts.bucket}/{mask_sts.file_key}"
        resp = BaseClient.put(url, {}, data)
        if resp.status_code != 200:
            raise ValueError(f"注册图形提示服务出错: {resp.status_code} {resp.content.decode(encoding='utf-8')}")
        else:
            resp_content = resp.content.decode('utf-8')
            resp_object = json.loads(resp_content)
            success = resp_object.get('success', False)
            if not success:
                raise ValueError(f"注册图形提示服务出错: {resp_content}")
            module = resp_object.get("module")
            resp_body_object = PublishOrUpdateAiesegVisualPromptResponseBody(AiesegVisualPrompt(prompt_id=module['id'],
                                                                                                prompt_name=module[
                                                                                                    'name'],
                                                                                                create_date_timestamp=
                                                                                                module[
                                                                                                    'createDate'],
                                                                                                modified_date_timestamp=
                                                                                                module[
                                                                                                    'modifiedDate'],
                                                                                                bg_image_url=module[
                                                                                                    'backgroundImage'],
                                                                                                mask_image_url=module[
                                                                                                    'maskImage']))
            return PublishOrUpdateAiesegVisualPromptResponse({}, 200, resp_body_object)

    def get_aieseg_visual_prompt(self, request: GetAiesegVisualPromptRequest) -> GetAiesegVisualPromptResponse:
        """
        查询图形提示
        :param request: 查询请求参数 `~GetAiesegVisualPromptRequest`
        :return: 查询到的图形提示list
        """

        url = get_host() + f"/mariana/openapi/mariana/aieseg/prompts"

        queries = dict()
        if request.prompt_id:
            queries['promptId'] = request.prompt_id
        if request.page_no:
            queries['pageNo'] = str(request.page_no)
        if request.page_size:
            queries['pageSize'] = str(request.page_size)
        if request.name_like:
            queries['nameLike'] = request.name_like
        if request.add_date_start:
            queries['addDateStartInSec'] = str(int(request.add_date_start.timestamp()))
        if request.add_date_end:
            queries['addDateEndInSec'] = str(int(request.add_date_end.timestamp()))
        if request.modified_date_start:
            queries['modifiedDateStartInSec'] = str(int(request.modified_date_start.timestamp()))
        if request.modified_date_end:
            queries['modifiedDateEndInSec'] = str(int(request.modified_date_end.timestamp()))

        if len(queries) > 0:
            url += "?"
        params = [f"{key}={parse.quote(value)}" for key, value in queries.items()]
        url += "&".join(params)

        logger.debug(f"查询图形提示 url: {url}")
        resp = BaseClient.get(url, {})
        if resp.status_code != 200:
            raise ValueError(f"获取图形提示服务出错: {resp.status_code} {resp.content.decode(encoding='utf-8')}")
        else:
            resp_content = resp.content.decode('utf-8')
            logger.debug(f"完成查询图形提示,, resp: {resp_content}")
            resp_object = json.loads(resp_content)
            success = resp_object.get('success', False)
            if not success:
                raise ValueError(f"获取图形提示服务出错: {resp_content}")
            module = resp_object.get("module")

            if module.get('total', 0) == 0 or len(module.get('list', [])) == 0:
                return GetAiesegVisualPromptResponse({}, 200, GetAiesegVisualPromptResponseBody(
                    page_no=request.page_no, page_size=request.page_size, pages=0, total=0, value_list=[]))
            else:
                return GetAiesegVisualPromptResponse({}, 200, GetAiesegVisualPromptResponseBody(
                    module['pageNo'], module['pageSize'], module['pages'], module['total'],
                    [AiesegVisualPrompt(prompt_id=l['id'],
                                        prompt_name=l['name'],
                                        create_date_timestamp=l['createDate'],
                                        modified_date_timestamp=l['modifiedDate'],
                                        bg_image_url=l['backgroundImage'],
                                        mask_image_url=l['maskImage']) for l in module['list']]
                ))

    def publish_aieseg_prompt(self,
                              request: PublishAiesegVisualPromptRequest) -> PublishOrUpdateAiesegVisualPromptResponse:
        """
        发布一个图形提示到aie平台
        :param request: 请求参数 `~PublishAiesegVisualPromptRequest`
        :return: 发布结果，包含了图形提示的平台ID
        """

        check_bg_mask(request.bg_image)
        check_bg_mask(request.mask_image)

        # save mask file to local
        mask_local_file_path = request.mask_image
        if isinstance(request.mask_image, ndarray):
            mask_local_file_path = tempfile.NamedTemporaryFile(suffix=".png").name
            logger.debug(f"Mask影像是ndarray，写入到本地文件 {mask_local_file_path}")
            cv2.imwrite(mask_local_file_path, request.mask_image)

        # save bg image file to local
        bg_local_file_path = request.bg_image
        if isinstance(request.bg_image, ndarray):
            bg_local_file_path = tempfile.NamedTemporaryFile(suffix=".png").name
            logger.debug(f"Background影像是ndarray，写入到本地文件 {bg_local_file_path}")
            cv2.imwrite(bg_local_file_path, request.bg_image)

        # upload to oss
        # get bgImgSts
        bg_sts: StsToken = get_sts_object(splitext(bg_local_file_path)[1][1:], DataType.AIESEG)
        # get maskImgSts
        mask_sts: StsToken = get_sts_object("png", DataType.AIESEG)
        logger.debug(f"上传background影像信息到{bg_sts.bucket}/{bg_sts.file_key}中...")
        do_oss_upload(bg_sts, bg_local_file_path)
        logger.debug(f"上传mask影像信息到{mask_sts.bucket}/{mask_sts.file_key}中...")
        do_oss_upload(mask_sts, mask_local_file_path)
        logger.debug("完成影像信息上传")

        # call registering
        url = get_host() + f"/mariana/openapi/mariana/aieseg/prompts"
        data = {
            "name": request.name,
            "backgroundFileUri": f"oss://{bg_sts.bucket}/{bg_sts.file_key}",
            "maskFileUri": f"oss://{mask_sts.bucket}/{mask_sts.file_key}"
        }
        logger.debug(f"发布AIESEG图形提示, 参数 {json.dumps(data)} ...")
        resp = BaseClient.post(url, {}, data)
        if resp.status_code != 200:
            raise ValueError(f"注册图形提示服务出错: {resp.status_code} {resp.content.decode(encoding='utf-8')}")
        else:
            resp_content = resp.content.decode('utf-8')
            resp_object = json.loads(resp_content)
            success = resp_object.get('success', False)
            if not success:
                raise ValueError(f"注册图形提示服务出错: {resp_content}")
            module = resp_object.get("module")
            resp_body_object = PublishOrUpdateAiesegVisualPromptResponseBody(AiesegVisualPrompt(prompt_id=module['id'],
                                                                                                prompt_name=module[
                                                                                                    'name'],
                                                                                                create_date_timestamp=
                                                                                                module[
                                                                                                    'createDate'],
                                                                                                modified_date_timestamp=
                                                                                                module[
                                                                                                    'modifiedDate'],
                                                                                                bg_image_url=module[
                                                                                                    'backgroundImage'],
                                                                                                mask_image_url=module[
                                                                                                    'maskImage']))
            logger.debug(f"完成发布AIESEG图形提示, 返回 {resp_content}")
            return PublishOrUpdateAiesegVisualPromptResponse({}, 200, resp_body_object)

    def generate_aieseg_visual_prompt(self,
                                      request: GenerateAieSegVisualPromptRequest) -> GenerateAieSegVisualPromptResponse:
        """
        调用服务创建一个图形提示
        :param request: 图形提示生成的参数 `~GenerateAieSegVisualPromptRequest`
        :return: 生成的图形提示的mask ndarray
        """

        if isinstance(request.image, ndarray):
            bg_file_path = None
        elif isinstance(request.image, str):
            if not os.path.isfile(request.image):
                raise ValueError(f"image 本地地址 {request.image}不存在")
            logger.debug(f"image是本地文件, 读取文件到ndarray中")
            bg_file_path = request.image
            request.image = cv2.imread(bg_file_path)
        else:
            raise ValueError(f"不支持的参数类型 image {type(request.image)}")

        check_bg_mask(request.image)

        if xor(request.points is None, request.point_labels is None):
            raise ValueError(f"参数 points 和 points_labels 需要同时存在")

        if request.points and request.point_labels:
            # check points
            for point in request.points:
                if not isinstance(point, (List, Tuple)) or len(point) != 2:
                    raise ValueError(f"参数points的格式为 [[123, 234]]")
            request.points = [list(map(int, p)) for p in request.points]

            # check point labels
            if len(request.points) != len(request.point_labels):
                raise ValueError(f"参数 points 和 point_lables 的长度需要相等")
            for label in request.point_labels:
                if label not in (0, 1):
                    raise ValueError(f"参数point_labels只接受0或者1的值")

        if all((request.points is None, request.bboxes is None)):
            raise ValueError("points 或者 bbox必须至少存在一个")

        # check bbox
        if request.bboxes and not isinstance(request.bboxes, (List, Tuple)):
            raise ValueError(f"参数bboxes的格式为 [[1, 2, 3, 4]]")
        if request.bboxes:
            for bbox in request.bboxes:
                valid_bbox(bbox)
            request.bboxes = [list(map(int, bbox)) for bbox in request.bboxes]
        else:
            request.bboxes = None

        # 判断point
        if request.points:
            img_shape = request.image.shape
            for (x, y) in request.points:
                if x > img_shape[1] or y > img_shape[0]:
                    raise ValueError(f"不合法的point {x} {y} img shape: {img_shape}")

        logger.debug(f"请求生成aieseg-mask")
        img = request.image

        # upload ndarray content to oss
        # upload to oss
        # get bgImgSts
        bg_sts: StsToken = get_sts_object('ndarray', DataType.AIESEG)
        do_oss_upload_from_bytes(bg_sts, base64.b64encode(img.tobytes()))

        url = f"{get_host()}/aie-seg-ref-predict"
        data = {
            "openapi": {
                "ref_img": {
                    "bg_array_oss_uri": f"oss://{bg_sts.bucket}/{bg_sts.file_key}",
                    "shape": list(img.shape),
                    "dtype": str(img.dtype)
                },
                "points": request.points,
                "point_labels": request.point_labels,
                "bboxes": request.bboxes if request.bboxes else []
            }
        }
        resp = BaseClient.post(url, {}, data)
        predict: np.ndarray = np.frombuffer(base64.b64decode(resp.json()["outputs"]["base64_array"]),
                                            dtype="uint8").reshape((img.shape[0], img.shape[1]))
        logger.debug("完成生成aieseg-mask")

        return GenerateAieSegVisualPromptResponse({}, 200, GenerateAieSegVisualPromptResponseBody(predict))
