from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from bson.objectid import ObjectId

from surebets_finder.shared.category import Category
from surebets_finder.shared.provider import Provider
from surebets_finder.shared.reflection import raises


@dataclass
class Bet:
    id: ObjectId
    opponent_1: str
    opponent_2: str
    odds_1: Decimal
    odds_2: Decimal
    category: Category
    provider: Provider
    date: datetime
    url: str
    updated_at: datetime
    created_at: datetime = datetime.utcnow()

    @raises(ValueError)
    def get_full_url(self) -> str:
        if self.provider == Provider.EFORTUNA:
            return f"https://www.efortuna.pl{self.url}"

        if self.provider == Provider.BETCLICK:
            return f"https://www.betclic.pl/{self.url}"

        if self.provider == Provider.LVBET:
            return f"https://lvbet.pl/en/pre-matches/{self.url}"

        raise ValueError(f"Provider `{self.provider}` is not correct!")
