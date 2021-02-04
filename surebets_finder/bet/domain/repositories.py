from typing import Any, Dict, List, Protocol

from bson.objectid import ObjectId

from surebets_finder.bet.domain.entities import Bet, SureBet


class BetRepository(Protocol):  # pragma: no cover
    def get(self, bet_id: ObjectId) -> Bet:
        ...

    def create(self, bet: Bet) -> None:
        ...

    def get_all_which_are_in_future(self) -> List[Bet]:
        ...

    def find_one(self, params: Dict[str, Any]) -> Bet:
        ...

    def save(self, bet: Bet) -> None:
        ...


class SureBetRepository(Protocol):
    def create(self, sure_bet: SureBet) -> None:
        ...

    def get_all(self) -> List[SureBet]:
        ...
