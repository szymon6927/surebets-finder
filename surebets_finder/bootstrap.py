import os
from logging import Logger

from kink import di
from pymongo import MongoClient
from pymongo.database import Database

from surebets_finder.logger import create_logger
from surebets_finder.raw_content.domain.repositories import RawContentRepository
from surebets_finder.raw_content.infrastructure.mongodb_raw_content_repo import MongoDBRawContentRepository


def bootstrap_di() -> None:
    print("in bootstrap_di")

    host = os.getenv("MONGO_HOST", "mongo")

    di[Logger] = create_logger()
    di[MongoClient] = lambda _: MongoClient(f"mongodb://{host}:27017/sure_bets")
    di[Database] = lambda _di: _di[MongoClient].sure_bets

    di[RawContentRepository] = lambda _di: MongoDBRawContentRepository(_di[Database])
