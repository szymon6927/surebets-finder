from logging import Logger
from typing import List

from bson.objectid import ObjectId
from kink import inject

from surebets_finder.raw_content.aplication.clients.betclick_client import BetClickClient
from surebets_finder.raw_content.aplication.clients.client import IWebClient
from surebets_finder.raw_content.aplication.clients.efortuna_client import EFortunaClient
from surebets_finder.raw_content.aplication.clients.lvbet_client import LvBetClient
from surebets_finder.raw_content.aplication.url_factory import UrlFactory
from surebets_finder.raw_content.domain.entities import RawContent
from surebets_finder.raw_content.domain.repositories import RawContentRepository
from surebets_finder.shared.category import Category
from surebets_finder.shared.provider import Provider


@inject
class Importer:
    def __init__(self, repository: RawContentRepository, logger: Logger) -> None:
        self._repository = repository
        self._logger = logger

    def _get_client(self, provider: Provider, urls: List[str]) -> IWebClient:
        mapper = {
            Provider.EFORTUNA: EFortunaClient(urls),  # type: ignore
            Provider.LVBET: LvBetClient(urls),  # type: ignore
            Provider.BETCLICK: BetClickClient(urls),  # type: ignore
        }

        return mapper[provider]

    def import_all(self) -> None:
        self._logger.info("Importer has started!")

        for provider in Provider:
            for category in Category:
                urls = UrlFactory.create(provider, category).get_urls()

                client = self._get_client(provider, urls)

                self._logger.info(
                    f"Importing data from category={category.value} and provider={provider.value} using {str(client)}"
                )

                content = client.get_raw_data()

                raw_content = RawContent(id=ObjectId(), content=content, category=category, provider=provider)

                self._repository.create(raw_content)
