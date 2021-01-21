import os
from typing import Iterator

import pytest
from kink import di
from pymongo.database import Database
from pymongo.mongo_client import MongoClient


@pytest.fixture(autouse=True)
def mongodb() -> Iterator[Database]:

    host = os.getenv("MONGO_HOST", "localhost")
    di[MongoClient] = MongoClient(f"mongodb://{host}:27017/sure_bets")
    di[Database] = di[MongoClient].perks

    yield di[Database]

    di[MongoClient].drop_database("sure_bets")
