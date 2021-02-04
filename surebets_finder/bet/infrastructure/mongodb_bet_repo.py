from dataclasses import asdict
from datetime import date, datetime, time
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum
from typing import Any, Dict, List

from bson import Decimal128
from bson.objectid import ObjectId
from kink import inject
from pymongo.database import Database

from surebets_finder.bet.domain.entities import Bet
from surebets_finder.bet.domain.errors import BetNotFoundError
from surebets_finder.bet.domain.repositories import BetRepository
from surebets_finder.shared.category import Category
from surebets_finder.shared.provider import Provider
from surebets_finder.shared.reflection import raises
from surebets_finder.shared.serializers import dataclass_serializer


@inject(alias=BetRepository)
class MongoDBBetRepository(BetRepository):
    def __init__(self, database: Database) -> None:
        self._collection = database["bet"]

    def _to_entity(self, document: Dict[str, Any]) -> Bet:
        return Bet(
            id=document["_id"],
            opponent_1=document["opponent_1"],
            opponent_2=document["opponent_2"],
            odds_1=document["odds_1"].to_decimal(),
            odds_2=document["odds_2"].to_decimal(),
            category=Category(document["category"]),
            provider=Provider(document["provider"]),
            date=document["date"],
            url=document["url"],
            updated_at=document["updated_at"],
            created_at=document["created_at"],
        )

    @raises(BetNotFoundError)
    def get(self, bet_id: ObjectId) -> Bet:
        document = self._collection.find_one({"_id": bet_id})

        if not document:
            raise BetNotFoundError(f"Bet with id `{bet_id}` does not exist.")

        return self._to_entity(document)

    def create(self, bet: Bet) -> None:
        document = asdict(bet, dict_factory=dataclass_serializer)

        document["_id"] = document.pop("id")

        self._collection.insert_one(document)

    def get_all_which_are_in_future(self) -> List[Bet]:
        today_date = date.today()
        date_time = datetime.combine(today_date, time.min)

        documents = self._collection.find({"date": {"$gte": date_time}})

        return [self._to_entity(document) for document in documents]

    @raises(BetNotFoundError)
    def find_one(self, params: Dict[str, Any]) -> Bet:
        document = self._collection.find_one(params)

        if not document:
            raise BetNotFoundError(f"Bet with params `{params}` does not exist.")

        return self._to_entity(document)

    def save(self, bet: Bet) -> None:
        query = {"_id": bet.id}
        to_update = {
            "$set": {
                "opponent_1": bet.opponent_1,
                "opponent_2": bet.opponent_2,
                "odds_1": self._to_decimal_128(bet.odds_1),
                "odds_2": self._to_decimal_128(bet.odds_2),
                "category": bet.category.value,
                "provider": bet.provider.value,
                "date": bet.date,
                "url": bet.url,
                "updated_at": datetime.utcnow(),
            }
        }

        self._collection.update_one(query, to_update)
