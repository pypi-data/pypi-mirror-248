import logging
from datetime import datetime
from typing import Union, Tuple, List, Dict

from numpy import ndarray

from aiearth.openapi.client._utils import milli_sec_2_datetime
from aiearth.openapi.enums import AiesegJobType
from aiearth.openapi.models import RasterParam, MapServiceParam, BaseToMapFromMapValidTeaModel
from aiearth.openapi.utils import read_from_url

logger = logging.getLogger("openapi")


class CreateAiesegJobRequest(BaseToMapFromMapValidTeaModel):
    """使用栅格影像等，创建一个aieseg解译任务"""

    def __init__(self,
                 aieseg_job_type: AiesegJobType,
                 input: Union[RasterParam, MapServiceParam],
                 job_name: str,
                 confidence: int = 80,
                 project_id: int = None,
                 filter_shape_data_id: str = None,
                 filter_shape_wkt: str = None,
                 pixel_threshold: int = None,
                 visual_prompt_id: str = None,
                 text_prompt: List[str] = None,
                 ):
        """
        创建AIESEG任务的参数
        :param aieseg_job_type:         AIESEG任务的类型，分单要素（目标）提取和全要素提取两种 `~AiesegJobType`
        :param input:                   输入的提取目标影像，可以使栅格文件或者ogc地图服务
        :param job_name:                任务的名称
        :param confidence               置信度
        :param project_id:              任务归属的项目空间id
        :param filter_shape_data_id:    任务框选的范围，选定矢量影像的dataId; 参数与filter_shape_wkt二选一，优先使用 filter_shape_data_id
        :param filter_shape_wkt:        任务框选的范围，使用矢量的wkt；参数与filter_shape_data_id二选一，优先使用 filter_shape_data_id
        :param pixel_threshold:         像素个数阈值；当目标像素个数小于该值时，则不提取；默认50像素
        :param visual_prompt_id:        图形提示ID，当 aieseg_job_type 为aie_seg_prompt时，visual_prompt_id 和 text_prompt选填一个，优先使用图形提示；否则不需要填写
        :param text_prompt:             文字提示，当 aieseg_job_type 为aie_seg_prompt时，visual_prompt_id 和 text_prompt选填一个，优先使用图形提示；否则不需要填写
        """
        self.aieseg_job_type = aieseg_job_type
        self.input = input
        self.job_name = job_name
        self.project_id = project_id

        if not job_name or len(job_name.strip()) < 1:
            raise ValueError("job_name 不可为空")

        if filter_shape_data_id is not None and filter_shape_wkt is not None:
            logger.warning(
                f"参数 filter_shape_data_id 与 filter_shape_wkt 只需提供一个，当两个参数都不为空时，默认使用 filter_shape_data_id")
        self.filter_shape_data_id = filter_shape_data_id
        self.filter_shape_wkt = filter_shape_wkt

        if aieseg_job_type == AiesegJobType.AIE_SEG_PANOPTIC and any(
                (pixel_threshold is not None, visual_prompt_id is not None, text_prompt is not None)):
            logger.warning(
                f"当使用 {AiesegJobType.AIE_SEG_PANOPTIC.name} 时，参数 pixel_threshold, visual_prompt_id, text_prompt 会被忽略")

        if aieseg_job_type == AiesegJobType.AIE_SEG_PANOPTIC and (confidence < 0 or confidence > 100):
            raise ValueError(f"当使用 {AiesegJobType.AIE_SEG_PANOPTIC.name} 时，confidence 值应在0-100之间")

        if text_prompt is not None and len(text_prompt) > 1:
            logger.warning(f"参数 text_prompt 目前仅支持第一个，更多支持正在迭代中...")

        if aieseg_job_type == AiesegJobType.AIE_SEG_PROMPT \
            and visual_prompt_id and text_prompt:
            logger.warning(f"当使用{AiesegJobType.AIE_SEG_PROMPT.name}时，visual_prompt_id, text_prompt 只需提供一个，当两个参数都不为空时，优先使用 visual_prompt_id")

        self.pixel_threshold = pixel_threshold
        self.visual_prompt_id = visual_prompt_id
        self.text_prompt = text_prompt
        self.confidence = confidence


class DeleteAiesegVisualPromptResponseBody(BaseToMapFromMapValidTeaModel):

    def __init__(self, deleted: bool):
        self.deleted = deleted


class DeleteAiesegVisualPromptResponse(BaseToMapFromMapValidTeaModel):
    """
    图形提示是否删除成功
    """

    def __init__(self, headers: Dict[str, str] = None,
                 status_code: int = None,
                 body: DeleteAiesegVisualPromptResponseBody = None):
        self.headers = headers
        self.status_code = status_code
        self.body = body


class DeleteAiesegVisualPromptRequest(BaseToMapFromMapValidTeaModel):
    """
    删除一个图形提示的请求
    """

    def __init__(self, prompt_id: str):
        """
        删除图形提示的请求参数
        :param prompt_id: 图形提示的平台ID
        """
        self.prompt_id = prompt_id


class AiesegVisualPrompt(BaseToMapFromMapValidTeaModel):
    """
    一个平台管理的图形提示
    """

    def __init__(self,
                 prompt_id: str,
                 prompt_name: str,
                 create_date_timestamp: int,
                 modified_date_timestamp: int,
                 bg_image_url: str,
                 mask_image_url: str):
        """
        一个平台管理的图形提示
        :param prompt_id: 图形提示ID
        :param prompt_name: 图形提示的名称
        :param create_date_timestamp: 图形提示创建的时间
        :param modified_date_timestamp: 图形提示上次修改的时间
        :param bg_image_url: 图形提示背景图可访问URL，有效期为获得后 10s; 可以访问 bg_image获取ndarray的表达
        :param mask_image_url: 图形提示mask可访问URL，有效期为获得后 10s；可以访问 mask_image获取ndarray的表达
        """
        self.prompt_id = prompt_id
        self.prompt_name = prompt_name
        self.create_datetime = milli_sec_2_datetime(create_date_timestamp)
        self.modified_datetime = milli_sec_2_datetime(modified_date_timestamp)
        # self.bg_image_url = bg_image_url
        # self.mask_image_url = mask_image_url

        self.bg_image = read_from_url(bg_image_url)
        self.mask_image = read_from_url(mask_image_url)


class UpdateAiesegVisualPromptRequest(BaseToMapFromMapValidTeaModel):
    """
    更新图形提示的请求参数
    """

    def __init__(self,
                 prompt_id: str,
                 name: str = None,
                 bg_image: Union[ndarray, str] = None,
                 mask_image: Union[ndarray, str] = None):
        """
        更新图形提示的请求参数
        :param prompt_id: 图形提示的平台ID
        :param name: 图形提示的名称
        :param bg_image: 图形提示的背景图 str 本地图片，ndarray需要shape为 (height, width, 3)
        :param mask_image: 图形提示的mask str 本地图片，ndarray需要shape为 (height, width)
        """

        if len(prompt_id.strip()) < 1:
            raise ValueError("不合法的图形提示ID")
        self.prompt_id = prompt_id

        if name is not None and len(name.strip()) < 1:
            logger.warning(f"更新aieseg图形提示的name参数 {name} 有效长度为0，将会被忽略")
            name = None

        if all((bg_image is None, name is None, mask_image is None)):
            raise ValueError("没有任何更新")

        self.name = name
        self.bg_image = bg_image
        self.mask_image = mask_image


class GetAiesegVisualPromptResponseBody(BaseToMapFromMapValidTeaModel):

    def __init__(self, page_no: int, page_size: int,
                 pages: int, total: int, value_list: List[AiesegVisualPrompt]):
        self.page_no = page_no
        self.page_size = page_size
        self.pages = pages
        self.total = total
        self.list = value_list


class GetAiesegVisualPromptResponse(BaseToMapFromMapValidTeaModel):

    def __init__(self, headers: Dict[str, str] = None,
                 status_code: int = None,
                 body: GetAiesegVisualPromptResponseBody = None):
        self.headers = headers
        self.status_code = status_code
        self.body = body


class GetAiesegVisualPromptRequest(BaseToMapFromMapValidTeaModel):
    """
    查询平台上管理的图形提示
    """

    def __init__(self,
                 prompt_id: str = None,
                 name_like: str = None,
                 page_no: int = 1,
                 page_size: int = 8,
                 add_date_start: datetime = None,
                 add_date_end: datetime = None,
                 modified_date_start: datetime = None,
                 modified_date_end: datetime = None):
        """
        查询参数
        :param prompt_id:               图形提示ID
        :param name_like:               图形提示的名称
        :param page_no:                 查询分页的页码，默认为1
        :param page_size:               查询分页的每页数量，默认为8
        :param add_date_start:          图形提示发布的日期开始
        :param add_date_end:            图形提示发布的日期的结束
        :param modified_date_start:     图形提示修改的日期的开始
        :param modified_date_end:       图形提示修改的日期的结束
        """
        self.prompt_id = prompt_id
        self.name_like = name_like
        self.page_no = page_no
        self.page_size = page_size
        self.add_date_start = add_date_start
        self.add_date_end = add_date_end
        self.modified_date_start = modified_date_start
        self.modified_date_end = modified_date_end


class PublishOrUpdateAiesegVisualPromptResponseBody(BaseToMapFromMapValidTeaModel):

    def __init__(self,
                 visual_prompt: AiesegVisualPrompt):
        self.visual_prompt = visual_prompt


class PublishOrUpdateAiesegVisualPromptResponse(BaseToMapFromMapValidTeaModel):

    def __init__(self, headers: Dict[str, str] = None,
                 status_code: int = None,
                 body: PublishOrUpdateAiesegVisualPromptResponseBody = None):
        self.headers = headers
        self.status_code = status_code
        self.body = body


class PublishAiesegVisualPromptRequest(BaseToMapFromMapValidTeaModel):
    """
    发布一个prompt图形提示的结果，进行管理起来
    一般用于对打点提示效果满意后，上传平台进行管理。
    """

    def __init__(self,
                 bg_image: Union[ndarray, str],
                 mask_image: Union[ndarray, str],
                 name: str):
        """
        创建请求
        :param bg_image: 图形提示背景图片，可以为本地图片或者是ndarray shape要求：(height, width, 3)
        :param mask_image: 图形提示mask图片，可以为本地图片或者是ndarray shape要求：(height, width)
        :param name: 图形提示名称
        """
        self.name = name
        self.bg_image = bg_image
        self.mask_image = mask_image


class GenerateAieSegVisualPromptResponseBody(BaseToMapFromMapValidTeaModel):
    """
    生成prompt图形提示的结果
    """

    def __init__(self, mask: ndarray):
        self.mask = mask


class GenerateAieSegVisualPromptResponse(BaseToMapFromMapValidTeaModel):
    """
    生成prompt图形提示的结果
    """

    def __init__(self, headers: Dict[str, str] = None,
                 status_code: int = None,
                 body: GenerateAieSegVisualPromptResponseBody = None):
        self.headers = headers
        self.status_code = status_code
        self.body = body


class GenerateAieSegVisualPromptRequest(BaseToMapFromMapValidTeaModel):
    """
    使用图片和关注点得到AIE Seg图形提示
    """

    def __init__(self,
                 image: Union[str, ndarray],
                 points: Union[List, Tuple] = None,
                 point_labels: Union[List, Tuple] = None,
                 bboxes: Union[List, Tuple] = None):
        """
        创建一个prompt生成的请求
        :param image: 影像的本地地址，或者ndarray 要求 shape (height, width, 3)， 其中 height, width 要求在 512, 1024之间
        :param points: 影像打点位置，格式要求为：[[282, 765]]
        :param point_labels: 影像打点positive, negative 表示; 0 表示negative，1表示positive，格式为：[1]
        :param bboxes: 框选一个范围，范围内的区域全部会被认为positive的目标: [[x1, y1, x2, y2]] 二维list, 左上角点坐标+右下角点坐标
        """
        self.image = image
        self.points = points
        self.point_labels = point_labels
        self.bboxes = bboxes
