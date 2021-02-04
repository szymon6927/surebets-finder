from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List

from bson.objectid import ObjectId

from surebets_finder.bet.domain.value_objects import InvestmentCalculationResult
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

    def __hash__(self) -> int:
        return hash((self.opponent_1, self.opponent_2, self.date))

    def __eq__(self, other: "Bet"):
        try:
            return (self.opponent_1, self.opponent_2, self.date) == (other.opponent_1, other.opponent_2, other.date)
        except AttributeError:
            return NotImplemented

    def __str__(self) -> str:
        return f"Bet(opponent_1={self.opponent_1}, opponent_2={self.opponent_2}, date={self.date}), provider={self.provider.value}"


@dataclass
class SureBet:
    id: ObjectId
    bets: List[ObjectId]
    opponent_1: str
    opponent_2: str
    odds_for_opponent_1: Decimal
    odds_for_opponent_2: Decimal
    url_1: str
    url_2: str
    opponent_1_winning: bool
    opponent_2_winning: bool
    calculation_result: InvestmentCalculationResult
    created_at: datetime = datetime.utcnow()

    def info(self) -> str:
        message_for_1_winning = f"""
        You have to bet
        {self.calculation_result.stake_1} for wining '{self.opponent_1}' ({self.odds_for_opponent_1}) on {self.url_1}
        (profit={self.calculation_result.profit_1}, benefit={self.calculation_result.benefit_1})
        and {self.calculation_result.stake_2} for loosing {self.opponent_2} ({self.odds_for_opponent_2}) on {self.url_2}
        (profit={self.calculation_result.profit_2}, benefit={self.calculation_result.benefit_2})
        """

        message_for_2_winning = f"""
        You have to bet
        {self.calculation_result.stake_1} for winning {self.opponent_2} ({self.odds_for_opponent_2}) on {self.url_2}
        (profit={self.calculation_result.profit_1}, benefit={self.calculation_result.benefit_1})
        and {self.calculation_result.stake_2} for loosing {self.opponent_1} ({self.odds_for_opponent_1}) on {self.url_1}
        (profit={self.calculation_result.profit_2}, benefit={self.calculation_result.benefit_2})
        """

        return message_for_1_winning if self.opponent_1_winning else message_for_2_winning

    def __str__(self) -> str:
        return f"SureBet(url_1={self.url_1}, url_2={self.url_2}, benefit_1={self.calculation_result.benefit_1}, benefit_2={self.calculation_result.benefit_2})"
