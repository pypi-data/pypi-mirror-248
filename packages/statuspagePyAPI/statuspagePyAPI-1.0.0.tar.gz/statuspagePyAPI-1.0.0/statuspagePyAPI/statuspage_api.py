# statuspage_api.py
from statuspagePyAPI.modules.components import Components

BASE_URL = 'https://api.statuspage.io/v1'


class StatusPageAPI:
    def __init__(self, api_key, raw_response: bool = False):
        self.api_key = api_key
        self.base_url = BASE_URL
        # 初始化其他必要的设置

        # 你可以在这里初始化各种模块
        self.components = Components(self.api_key, self.base_url, raw_response)

    # 添加一些通用方法或者属性
    # ...

# 如果需要，你可以在这个文件中实现其他辅助类或函数
