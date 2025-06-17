from gecko.config import settings


def get_url(path: str) -> str:
    return settings.api_url + path
