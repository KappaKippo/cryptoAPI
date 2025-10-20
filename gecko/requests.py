from gecko.config import settings
import requests


class RequestClient:
    api_key_header = {"x-cg-demo-api-key": settings.api_token}
    api_url = settings.api_url

    async def get(self, url: str, params: dict):
        response = requests.get(
            f"{self.api_url}{url}", params=params, headers=self.api_key_header
        )
        return response.json()
