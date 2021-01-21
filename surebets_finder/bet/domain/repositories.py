from typing import List, Protocol

from bson.objectid import ObjectId

from surebets_finder.bet.domain.entities import Bet


class BetRepository(Protocol):  # pragma: no cover
    def get(self, bet_id: ObjectId) -> Bet:
        ...

    def create(self, bet: Bet) -> None:
        ...

    def get_all_which_are_in_future(self) -> List[Bet]:
        ...
