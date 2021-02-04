from dataclasses import asdict
from typing import List

from kink import inject
from pymongo.database import Database

from surebets_finder.bet.domain.entities import SureBet
from surebets_finder.bet.domain.repositories import SureBetRepository
from surebets_finder.shared.serializers import dataclass_serializer


@inject(alias=SureBetRepository)
class MongoDBBetRepository(SureBetRepository):
    def __init__(self, database: Database) -> None:
        self._collection = database["sure_bet"]

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

    def create(self, sure_bet: SureBet) -> None:
        document = asdict(sure_bet, dict_factory=dataclass_serializer)

        document["_id"] = document.pop("id")

        self._collection.insert_one(document)

    def get_all(self) -> List[SureBet]:
        ...
