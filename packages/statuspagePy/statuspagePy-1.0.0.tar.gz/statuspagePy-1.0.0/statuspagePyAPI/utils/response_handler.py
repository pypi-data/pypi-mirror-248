class ResponseHandler:
    def __init__(self, raw_response: bool = False):
        self.raw_response = raw_response

    def process_response(self, response):
        """
        处理响应，根据全局配置返回 JSON 数据或 Response 对象
        """
        if self.raw_response:
            return response
        else:
            return response.json()
