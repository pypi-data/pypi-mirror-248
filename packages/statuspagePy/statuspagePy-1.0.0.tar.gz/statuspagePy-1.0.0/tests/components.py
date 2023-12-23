import unittest
from statuspagePyAPI.statuspage_api import StatusPageAPI

statusPageApi = StatusPageAPI(api_key='cbd01a00c9574c93b6bde36a57be4e76', raw_response=True)
page_id = 'c9v2yygbjg5l'


class MyTestCase(unittest.TestCase):

    def test_components_get(self):
        # 获取响应
        response = statusPageApi.components.get_components(page_id=page_id)

        # 打印响应（可选，仅用于调试）
        # print(response)

        # 检查 HTTP 状态码
        self.assertEqual(response.status_code, 200, "Failed to fetch components")

        # 如果需要，可以添加更多的断言来验证响应内容
        # 例如，检查返回的数据结构、数据内容等


if __name__ == '__main__':
    unittest.main()
