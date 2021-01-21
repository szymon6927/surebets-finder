from logging import Logger
from typing import List

import requests
from kink import inject

from surebets_finder.raw_content.aplication.clients.client import IWebClient
from surebets_finder.raw_content.domain.errors import RequestError


@inject
class LvBetClient(IWebClient):
    def __init__(self, urls: List[str], logger: Logger) -> None:
        self._urls = urls
        self._logger = logger

    def _make_request(self, url: str) -> str:
        try:
            response = requests.get(url=url, timeout=(2, 3))
            response.raise_for_status()

            return response.text
        except requests.exceptions.HTTPError as e:
            self._logger.exception(f"[lvbet.pl] HTTP Error! {str(e)}")
            raise RequestError("HTTP Error!") from e
        except requests.exceptions.ConnectionError as e:
            self._logger.exception(f"[lvbet.pl] Connection Error! {str(e)}")
            raise RequestError("Connection Error!") from e
        except requests.exceptions.Timeout as e:
            self._logger.exception(f"[lvbet.pl] Timeout Error! {str(e)}")
            raise RequestError("Timeout Error!") from e
        except requests.exceptions.RequestException as e:
            self._logger.exception(f"[lvbet.pl] Request Error! {str(e)}")
            raise RequestError("Request Error!") from e

    def get_raw_data(self) -> str:
        all_data = ""

        for url in self._urls:
            content = self._make_request(url)
            all_data += content

        return all_data

    def __str__(self) -> str:
        return "BetClickClient"
