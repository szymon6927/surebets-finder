from dataclasses import asdict
from enum import Enum
from typing import Any, Dict, List

from bson.objectid import ObjectId
from kink import inject
from pymongo.database import Database

from surebets_finder.raw_content.domain.entities import RawContent
from surebets_finder.raw_content.domain.errors import RawContentNotFoundError
from surebets_finder.raw_content.domain.repositories import RawContentRepository
from surebets_finder.shared.category import Category
from surebets_finder.shared.provider import Provider
from surebets_finder.shared.reflection import raises


@inject(alias=RawContentRepository)
class MongoDBRawContentRepository(RawContentRepository):
    def __init__(self, database: Database):
        self._collection = database["raw_content"]

    def _serialize(self, data: Any) -> Dict[Any, Any]:
        """Mainly for Enum serialization"""

        return {field: value.value if isinstance(value, Enum) else value for field, value in data}

    def _to_entity(self, document: Dict[str, Any]) -> RawContent:
        return RawContent(
            id=document["_id"],
            content=document["content"],
            category=Category(document["category"]),
            provider=Provider(document["provider"]),
            was_processed=document["was_processed"],
            created_at=document["created_at"],
        )

    @raises(RawContentNotFoundError)
    def get(self, raw_content_id: ObjectId) -> RawContent:
        document = self._collection.find_one({"_id": raw_content_id})

        if not document:
            raise RawContentNotFoundError(f"RawContent with id `{raw_content_id}` does not exist.")

        return self._to_entity(document)

    def create(self, raw_content: RawContent) -> None:
        document = asdict(raw_content, dict_factory=self._serialize)

        document["_id"] = document.pop("id")

        self._collection.insert_one(document)

    def get_all_unprocessed(self) -> List[RawContent]:
        documents = self._collection.find({"was_processed": True})

        return [self._to_entity(document) for document in documents]
