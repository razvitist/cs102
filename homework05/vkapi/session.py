import typing as tp

import requests
from requests.adapters import HTTPAdapter, Retry


class Session:
    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.session = requests.Session()
        adapter = HTTPAdapter(
            max_retries=Retry(
                total=max_retries,
                backoff_factor=backoff_factor,
                status_forcelist=(500, 502, 503, 504),
            )
        )
        self.session.mount("https://", adapter)
        self._timeout = timeout
        self._base_url = base_url

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        return self.session.get(url=f"{self._base_url}/{url}", params=kwargs, timeout=self._timeout)

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        return self.session.post(url=f"{self._base_url}/{url}", data=kwargs, timeout=self._timeout)
