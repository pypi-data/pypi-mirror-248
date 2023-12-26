from abc import ABC
from typing import Dict

from Tea.model import TeaModel


class BasePublishLocalResponseBody(TeaModel):

    def __init__(self, data_id: str = None, name: str = None):
        self.data_id = data_id
        self.name = name

    def validate(self):
        pass

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get("DataId") is not None:
            self.data_id = m.get('DataId')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        return self

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data_id is not None:
            result['DataId'] = self.data_id
        if self.name is not None:
            result['Name'] = self.name
        return result


class BasePublishLocalResponse(ABC, TeaModel):

    def __init__(self, headers: Dict[str, str] = None,
                 status_code: int = None,
                 body: BasePublishLocalResponseBody = None):
        self.headers = headers
        self.status_code = status_code
        self.body = body

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['Headers'] = self.headers
        if self.status_code is not None:
            result['StatusCode'] = self.status_code
        if self.body is not None:
            result['Body'] = self.body.to_map()
        return result

    def from_map(self, m=None):
        m = m or dict()
        if m.get('Headers') is not None:
            self.headers = m.get('Headers')
        if m.get('StatusCode') is not None:
            self.status_code = m.get('StatusCode')
        if m.get('Body') is not None:
            temp_model = BasePublishLocalResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class BasePublishLocalDoubleFileRequest(ABC, TeaModel):
    def __init__(self, main_file_path: str = None,
                 attach_file_path: str = None,
                 name: str = None,
                 acquisition_date: str = None):
        self.main_file_path = main_file_path
        self.attach_file_path = attach_file_path
        self.name = name
        self.acquisition_date = acquisition_date

    def from_map(self, m: dict = None):
        m = m or dict()

        if m.get('MainFilePath') is not None:
            self.main_file_path = m.get('MainFilePath')
        if m.get('AttachFilePath') is not None:
            self.attach_file_path = m.get('AttachFilePath')
        if m.get('Name') is not None:
            self.name = m.get('Name')
        if m.get('AcquisitionDate') is not None:
            self.acquisition_date = m.get('AcquisitionDate')
        return self

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.name is not None:
            result['Name'] = self.name
        if self.main_file_path is not None:
            result['MainFilePath'] = self.main_file_path
        if self.attach_file_path is not None:
            result['AttachFilePath'] = self.attach_file_path
        if self.acquisition_date is not None:
            result['AcquisitionDate'] = self.acquisition_date
        return result


class BasePublishLocalSingleFileRequest(ABC, TeaModel):

    def __init__(self, local_file_path: str = None,
                 name: str = None,
                 acquisition_date: str = None):
        self.local_file_path = local_file_path
        self.name = name
        self.acquisition_date = acquisition_date

    def validate(self):
        pass

    def from_map(self, m=None):
        m = m or dict()
        if m.get("LocalFilePath") is not None:
            self.local_file_path = m.get("localFilePath")
        if m.get("Name") is not None:
            self.name = m.get("name")
        if m.get("AcquisitionDate") is not None:
            self.acquisition_date = m.get("AcquisitionDate")
        return self

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.local_file_path is not None:
            result['LocalFilePath'] = self.local_file_path
        if self.name is not None:
            result['Name'] = self.name
        if self.acquisition_date is not None:
            result['AcquisitionDate'] = self.acquisition_date
        return result


class PublishLocalShapefileRequest(BasePublishLocalSingleFileRequest):

    def __init__(self, name: str = None,
                 local_file_path: str = None):
        super().__init__(local_file_path, name, None)


class PublishLocalShapefileResponse(BasePublishLocalResponse):
    def __init__(self, headers: Dict[str, str] = None,
                 status_code: int = None,
                 body: BasePublishLocalResponseBody = None):
        super().__init__(headers, status_code, body)


class PublishLocalTiffRequest(BasePublishLocalSingleFileRequest):
    def __init__(self, local_file_path: str = None,
                 name: str = None,
                 acquisition_date: str = None):
        super().__init__(local_file_path,
                         name,
                         acquisition_date)


class PublishLocalTiffResponse(BasePublishLocalResponse):

    def __init__(self, headers: Dict[str, str] = None,
                 status_code: int = None,
                 body: BasePublishLocalResponseBody = None):
        super().__init__(headers, status_code, body)


class PublishLocalImgRequest(BasePublishLocalSingleFileRequest):

    def __init__(self, local_file_path: str = None,
                 name: str = None,
                 acquisition_date: str = None):
        super().__init__(local_file_path,
                         name,
                         acquisition_date)


class PublishLocalImgResponse(BasePublishLocalResponse):

    def __init__(self, headers: Dict[str, str] = None,
                 status_code: int = None,
                 body: BasePublishLocalResponseBody = None):
        super().__init__(headers, status_code, body)


class PublishLocalImgIgeRequest(BasePublishLocalDoubleFileRequest):

    def __init__(self, main_file_path: str = None, attach_file_path: str = None, name: str = None,
                 acquisition_date: str = None):
        super().__init__(main_file_path, attach_file_path, name, acquisition_date)


class PublishLocalImgIgeResponse(BasePublishLocalResponse):

    def __init__(self, headers: Dict[str, str] = None, status_code: int = None,
                 body: BasePublishLocalResponseBody = None):
        super().__init__(headers, status_code, body)


class PublishLocalTiffRpbRequest(BasePublishLocalDoubleFileRequest):

    def __init__(self, main_file_path: str = None, attach_file_path: str = None, name: str = None,
                 acquisition_date: str = None):
        super().__init__(main_file_path, attach_file_path, name, acquisition_date)


class PublishLocalTiffRpbResponse(BasePublishLocalResponse):

    def __init__(self, headers: Dict[str, str] = None, status_code: int = None,
                 body: BasePublishLocalResponseBody = None):
        super().__init__(headers, status_code, body)


class PublishLocalTiffRpcRequest(BasePublishLocalDoubleFileRequest):
    def __init__(self, main_file_path: str = None, attach_file_path: str = None, name: str = None,
                 acquisition_date: str = None):
        super().__init__(main_file_path, attach_file_path, name, acquisition_date)


class PublishLocalTiffRpcResponse(BasePublishLocalResponse):

    def __init__(self, headers: Dict[str, str] = None, status_code: int = None,
                 body: BasePublishLocalResponseBody = None):
        super().__init__(headers, status_code, body)


class PublishLocalTiffTfwRequest(BasePublishLocalDoubleFileRequest):
    def __init__(self, main_file_path: str = None, attach_file_path: str = None, name: str = None,
                 acquisition_date: str = None):
        super().__init__(main_file_path, attach_file_path, name, acquisition_date)


class PublishLocalTiffTfwResponse(BasePublishLocalResponse):

    def __init__(self, headers: Dict[str, str] = None, status_code: int = None,
                 body: BasePublishLocalResponseBody = None):
        super().__init__(headers, status_code, body)