import os
from datetime import datetime, timedelta
from typing import Any, Dict, Iterator

import pytest
from bson import Decimal128
from bson.objectid import ObjectId
from kink import di
from pymongo.database import Database
from pymongo.mongo_client import MongoClient

from surebets_finder.shared.category import Category
from surebets_finder.shared.provider import Provider


@pytest.fixture
def dummy_raw_content_id() -> ObjectId:
    return ObjectId("6009cb62cd435afcacaee12c")


@pytest.fixture
def dummy_raw_content_document(dummy_raw_content_id: ObjectId) -> Dict[str, Any]:
    return {
        "_id": dummy_raw_content_id,
        "content": "some content",
        "category": Category.ESPORT.value,
        "provider": Provider.EFORTUNA.value,
        "was_processed": False,
        "created_at": datetime.utcnow(),
    }


@pytest.fixture
def dummy_bet_id() -> ObjectId:
    return ObjectId("6009dcc742a52b6b664198b4")


@pytest.fixture
def dummy_bet_document(dummy_bet_id: ObjectId) -> Dict[str, Any]:
    return {
        "_id": dummy_bet_id,
        "opponent_1": "test 1",
        "opponent_2": "test 2",
        "odds_1": Decimal128("4.12"),
        "odds_2": Decimal128("3.56"),
        "category": Category.ESPORT.value,
        "provider": Provider.EFORTUNA.value,
        "date": datetime.utcnow(),
        "url": "/test/bet/url",
        "updated_at": datetime.utcnow(),
        "created_at": datetime.utcnow(),
    }


@pytest.fixture(autouse=True)
def mongodb(dummy_raw_content_document: Dict[str, Any], dummy_bet_document: Dict[str, Any]) -> Iterator[Database]:
    host = os.getenv("MONGO_HOST", "localhost")

    mongo_client = MongoClient(f"mongodb://{host}:27017/test_sure_bets")
    mongo_db: Database = mongo_client.test_sure_bets

    di[MongoClient] = mongo_client
    di[Database] = mongo_db

    mongo_db["raw_content"].insert_one(dummy_raw_content_document)
    mongo_db["bet"].insert_one(dummy_bet_document)

    yield di[Database]

    di[MongoClient].drop_database("test_sure_bets")


@pytest.fixture()
def fill_in_db_with_some_processed_raw_contents(mongodb: Database) -> None:
    for i in range(5):
        mongodb["raw_content"].insert_one(
            {
                "_id": ObjectId(),
                "content": f"some content {i}",
                "category": Category.ESPORT.value,
                "provider": Provider.EFORTUNA.value,
                "was_processed": True,
                "created_at": datetime.utcnow(),
            }
        )


@pytest.fixture()
def fill_in_db_with_bets_which_are_in_future(mongodb: Database) -> None:
    for i in range(5):
        mongodb["bet"].insert_one(
            {
                "_id": ObjectId(),
                "opponent_1": f"opponent_1 {i}",
                "opponent_2": f"opponent_2 {i}",
                "odds_1": Decimal128("4.12"),
                "odds_2": Decimal128("3.56"),
                "category": Category.ESPORT.value,
                "provider": Provider.EFORTUNA.value,
                "date": datetime.utcnow() + timedelta(days=5),
                "url": "/test/bet/url",
                "updated_at": datetime.utcnow(),
                "created_at": datetime.utcnow(),
            }
        )
