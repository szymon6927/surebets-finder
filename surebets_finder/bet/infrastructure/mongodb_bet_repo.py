from dataclasses import asdict
from datetime import datetime
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


@inject(alias=BetRepository)
class MongoDBBetRepository(BetRepository):
    def __init__(self, database: Database):
        self._collection = database["bet"]

    def _serialize(self, data: Any) -> Dict[Any, Any]:
        serialized = dict()

        for field, value in data:
            if isinstance(value, Enum):
                serialized[field] = value.value
            elif isinstance(value, Decimal):
                value = Decimal(value.quantize(Decimal(".01"), rounding=ROUND_HALF_UP))
                serialized[field] = Decimal128(str(value))
            else:
                serialized[field] = value

        return serialized

    def _to_entity(self, document: Dict[str, Any]) -> Bet:
        return Bet(
            id=document["_id"],
            opponent_1=document["opponent_1"],
            opponent_2=document["opponent_2"],
            odds_1=Decimal(document["odds_1"]),
            odds_2=Decimal(document["odds_2"]),
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
        document = asdict(bet, dict_factory=self._serialize)

        document["_id"] = document.pop("id")

        self._collection.insert_one(document)

    def get_all_which_are_in_future(self) -> List[Bet]:
        documents = self._collection.find({"date": {"$gte": datetime.utcnow()}})

        return [self._to_entity(document) for document in documents]
