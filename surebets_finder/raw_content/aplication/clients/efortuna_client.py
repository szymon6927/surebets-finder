from logging import Logger
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup
from kink import inject
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from surebets_finder.raw_content.aplication.clients.client import IWebClient
from surebets_finder.raw_content.domain.errors import RequestError


@inject
class EFortunaClient(IWebClient):
    MAIN_HTML_DIV_ID = "main-content"

    def __init__(self, urls: List[str], logger: Logger) -> None:
        self._urls = urls
        self._logger = logger
        self._driver = self._build_chrome_web_driver()

    def _build_chrome_web_driver(self) -> WebDriver:
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        chrome_web_driver = webdriver.Chrome(
            ChromeDriverManager(path=self._get_browser_driver_install_path()).install(), chrome_options=chrome_options
        )

        return chrome_web_driver

    def _get_browser_driver_install_path(self) -> str:
        file_path = Path(__file__)

        return str(file_path.parent.parent.parent.parent / "browsers")

    def _make_request(self, url: str) -> str:
        try:
            self._driver.set_page_load_timeout(20)
            self._driver.get(url)
            return self._driver.page_source
        except TimeoutException as e:
            self._logger.exception(f"[efortuna.pl] Timeout Error! {str(e)}")
            self._driver.close()
            raise RequestError("Timeout Error! {str(e)}")

    def _extract_information(self, page_content: str) -> str:
        soup = BeautifulSoup(page_content, "html.parser")

        main_content = soup.find(id=self.MAIN_HTML_DIV_ID).prettify()
        main_content = main_content.replace('<div=""', "")

        return main_content

    def get_raw_data(self) -> str:
        all_data = ""

        for url in self._urls:
            content = self._make_request(url)
            filtered_content = self._extract_information(content)

            all_data += filtered_content

        return all_data

    def __str__(self) -> str:
        return "EFortunaClient"
