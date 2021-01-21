from datetime import datetime

import pytest
from bson.objectid import ObjectId
from pymongo.database import Database

from surebets_finder.raw_content.domain.entities import RawContent
from surebets_finder.raw_content.domain.errors import RawContentNotFoundError
from surebets_finder.raw_content.infrastructure.mongodb_raw_content_repo import MongoDBRawContentRepository
from surebets_finder.shared.category import Category
from surebets_finder.shared.provider import Provider


def test_can_create_raw_content(mongodb: Database) -> None:
    # given
    repo = MongoDBRawContentRepository()  # type: ignore

    # and
    raw_content = RawContent(
        id=ObjectId(), content="some content", category=Category.ESPORT, provider=Provider.EFORTUNA, was_processed=False
    )

    # when
    repo.create(raw_content)

    # then
    document = mongodb["raw_content"].find_one({"_id": raw_content.id})
    assert document["_id"] == raw_content.id
    assert document["content"] == raw_content.content


def test_can_get_raw_content(mongodb: Database) -> None:
    # given
    repo = MongoDBRawContentRepository()  # type: ignore

    # when
    raw_content_id = ObjectId()
    mongodb["raw_content"].insert_one(
        {
            "_id": raw_content_id,
            "content": "some content",
            "category": Category.ESPORT.value,
            "provider": Provider.EFORTUNA.value,
            "was_processed": False,
            "created_at": datetime.utcnow(),
        }
    )

    # and
    raw_content = repo.get(raw_content_id)

    # then
    assert isinstance(raw_content, RawContent)
    assert raw_content.id == raw_content_id
    assert raw_content.content == "some content"
    assert raw_content.category == Category.ESPORT
    assert raw_content.provider == Provider.EFORTUNA
    assert raw_content.was_processed is False


def test_get_raw_content_should_raise_an_exception_when_entity_does_not_exist(mongodb: Database) -> None:
    # given
    repo = MongoDBRawContentRepository()  # type: ignore

    # then
    with pytest.raises(RawContentNotFoundError):
        repo.get(ObjectId())


def test_can_save_raw_content(mongodb: Database, dummy_raw_content_id: ObjectId) -> None:
    # given
    repo = MongoDBRawContentRepository()  # type: ignore

    # when
    raw_content = repo.get(ObjectId(dummy_raw_content_id))

    # and
    raw_content.content = "some different content"

    # and
    repo.save(raw_content)

    # then
    document = mongodb["raw_content"].find_one({"_id": dummy_raw_content_id})
    assert document["content"] == "some different content"


@pytest.mark.usefixtures("fill_in_db_with_some_processed_raw_contents")
def test_can_get_all_unprocessed(mongodb: Database) -> None:
    # given
    repo = MongoDBRawContentRepository()  # type: ignore

    # when
    all_unprocessed = repo.get_all_unprocessed()

    # then
    assert len(all_unprocessed) == 1
