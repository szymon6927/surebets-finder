from dataclasses import dataclass
from decimal import Decimal


@dataclass
class SureBetCheckResult:
    is_sure_bet: bool
    for_opponent_1_winning: bool
    for_opponent_2_winning: bool


@dataclass
class InvestmentCalculationResult:
    stake_1: Decimal
    stake_2: Decimal
    profit_1: Decimal
    profit_2: Decimal
    benefit_1: str
    benefit_2: str
