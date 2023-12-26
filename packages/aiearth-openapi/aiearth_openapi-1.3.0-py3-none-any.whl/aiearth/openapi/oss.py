import os


class StsToken(object):

    def __init__(self, json_object: dict):
        self.access_key_id = json_object['accessKeyId']
        self.access_key_secret = json_object['accessKeySecret']
        self.bucket = json_object['bucket']
        self.expiration = json_object['expiration']
        self.file_key = json_object['fileKey']
        self.file_name = json_object['fileName']
        self.region = json_object['region']
        self.security_token = json_object['securityToken']
        self._endpoint: str = json_object['endpoint']

    @property
    def endpoint(self):
        region_id = os.getenv("ALIYUN_REGION_ID")
        if region_id is None:
            return self._endpoint

        ep_first_part = self._endpoint.split(".")[0]
        if region_id in ep_first_part:
            ep_first_part_internal = ep_first_part + "-internal"
            return self._endpoint.replace(ep_first_part, ep_first_part_internal)
        else:
            return self._endpoint
