from requests import get
from gecko.config import settings


class RequestsClient:
    API_KEY_HEADER = {"x-cg-api-key": settings.api_token}

    def __init__(
        self, url: str, params: dict | None = None, headers: dict | None = None
    ):
        self.url = url
        self.params = params
        self.headers = (
            self.API_KEY_HEADER if not headers else self.API_KEY_HEADER.update(headers)
        )

    def get(self):
        response = get(self.url, headers=self.headers, params=self.params)
        return response.json()
