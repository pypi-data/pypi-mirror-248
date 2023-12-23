import requests


class CustomSession(requests.Session):
    def __init__(self, api_key: str):
        super().__init__()
        self.headers.update({'Authorization': f'OAuth {api_key}'})