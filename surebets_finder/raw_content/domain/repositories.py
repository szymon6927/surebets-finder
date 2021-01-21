from typing import List, Protocol

from bson.objectid import ObjectId

from surebets_finder.raw_content.domain.entities import RawContent


class RawContentRepository(Protocol):  # pragma: no cover
    def get(self, raw_content_id: ObjectId) -> RawContent:
        ...

    def create(self, raw_content: RawContent) -> None:
        ...

    def get_all_unprocessed(self) -> List[RawContent]:
        ...

    def save(self, raw_content: RawContent) -> None:
        ...
