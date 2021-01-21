from dataclasses import dataclass
from logging import Logger
from typing import List

from bson.objectid import ObjectId
from kink import inject

from surebets_finder.raw_content.domain.entities import RawContent
from surebets_finder.raw_content.domain.repositories import RawContentRepository
from surebets_finder.shared.category import Category
from surebets_finder.shared.provider import Provider


@dataclass
class RawContentDTO:
    id: ObjectId
    content: str
    category: Category
    provider: Provider


@inject
class RawContentFacade:
    def __init__(self, repository: RawContentRepository, logger: Logger):
        self._repository = repository
        self._logger = logger

    def _to_dto(self, raw_content: RawContent) -> RawContentDTO:
        return RawContentDTO(
            id=raw_content.id, content=raw_content.content, category=raw_content.category, provider=raw_content.provider
        )

    def get_all_unprocessed_raw_contents(self) -> List[RawContentDTO]:
        self._logger.info("Getting all unprocessed raw contents")

        records = self._repository.get_all_unprocessed()

        return [self._to_dto(record) for record in records]

    def mark_raw_content_as_processed(self, raw_content_id: ObjectId) -> None:
        self._logger.info(f"Marking raw_content with id={raw_content_id} as processed")

        raw_content = self._repository.get(raw_content_id)

        raw_content.was_processed = True

        self._repository.save(raw_content)
