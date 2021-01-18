import os
from logging import Logger

from kink import di
from pymongo import MongoClient
from pymongo.database import Database

from surebets_finder.logger import create_logger


def bootstrap_di() -> None:
    host = os.getenv("MONGO_HOST", "mongo")

    di[Logger] = create_logger()
    di[MongoClient] = lambda _: MongoClient(f"mongodb://{host}:27017/sure_bets")
    di[Database] = lambda di_: di_[MongoClient].sure_bets
