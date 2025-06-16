from requests import get


class RequestsClient:
    def __init__(self, url: str, params: dict, headers: dict):
        self.url = url
        self.params = params
        self.headers = headers

    def get(self):
        response = get(self.url, headers=self.headers)
        return response.json()
