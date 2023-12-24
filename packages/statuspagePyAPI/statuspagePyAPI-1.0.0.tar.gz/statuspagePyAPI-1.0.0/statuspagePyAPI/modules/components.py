from typing import Dict, Any, Union

from requests import Response

from statuspagePyAPI.modules.custom_session import CustomSession
from statuspagePyAPI.utils.response_handler import ResponseHandler


class Components(ResponseHandler):
    def __init__(self, api_key: str, base_url: str, raw_response: bool = False):
        super().__init__(raw_response)
        self._api_key: str = api_key
        self._base_url: str = base_url
        self.session = CustomSession(api_key)

    def create_component(self, page_id: str, **kwargs: Any) -> Union[Dict[str, Any], Response]:
        """
        创建组件
        :param page_id: 页面ID
        :param kwargs: 详见 https://developer.statuspage.io/#operation/postPagesPageIdComponents
        :return: 返回创建的组件信息
        """
        url = f'{self._base_url}/pages/{page_id}/components'
        response = self.session.post(url, json=kwargs)
        return self.process_response(response)

    def get_components(self, page_id: str) -> Union[Dict[str, Any], Response]:
        """
        获取组件列表
        :param page_id: 页面ID
        :return: 返回组件列表
        """
        url = f'{self._base_url}/pages/{page_id}/components'
        response = self.session.get(url)
        return self.process_response(response)

    def update_component(self, page_id: str, component_id: str, **kwargs: Any) -> Union[Dict[str, Any], Response]:
        """
        更新组件
        :param page_id: 页面ID
        :param component_id: 组件ID
        :param kwargs: 详见 https://developer.statuspage.io/#operation/patchPagesPageIdComponentsComponentId
        :return: 返回更新后的组件信息
        """
        url = f'{self._base_url}/pages/{page_id}/components/{component_id}'
        response = self.session.patch(url, json=kwargs)
        return self.process_response(response)

    def delete_component(self, page_id: str, component_id: str) -> Union[Dict[str, Any], Response]:
        """
        删除组件
        :param page_id: 页面ID
        :param component_id: 组件ID
        :return: 返回删除的组件信息
        """
        url = f'{self._base_url}/pages/{page_id}/components/{component_id}'
        response = self.session.delete(url)
        return self.process_response(response)

    def get_component(self, page_id: str, component_id: str) -> Union[Dict[str, Any], Response]:
        """
        获取组件信息
        :param page_id: 页面ID
        :param component_id: 组件ID
        :return: 返回组件信息
        """
        url = f'{self._base_url}/pages/{page_id}/components/{component_id}'
        response = self.session.get(url)
        return self.process_response(response)

    def get_uptime(self, page_id: str, component_id: str) -> Union[Dict[str, Any], Response]:
        """
        获取组件的可用性
        :param page_id: 页面ID
        :param component_id: 组件ID
        :return: 返回组件的可用性
        """
        url = f'{self._base_url}/pages/{page_id}/components/{component_id}/uptime'
        response = self.session.get(url)
        return self.process_response(response)
