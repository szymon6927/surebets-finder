import itertools
from datetime import datetime
from decimal import Decimal
from logging import Logger

from bson.objectid import ObjectId
from kink import inject
from sympy import Eq, solve, symbols

from surebets_finder.bet.domain.entities import Bet, SureBet
from surebets_finder.bet.domain.repositories import BetRepository
from surebets_finder.bet.domain.value_objects import InvestmentCalculationResult, SureBetCheckResult


@inject
class SureBetsFinder:
    def __init__(self, logger: Logger, repository: BetRepository):
        self._logger = logger
        self._repository = repository

    def _is_surebet(self, bet_1: Bet, bet_2: Bet) -> SureBetCheckResult:
        self._logger.info(f"Checking surebet formula for {bet_1.odds_1} and {bet_2.odds_2}")

        if (1 / bet_1.odds_1) + (1 / bet_2.odds_2) < 1.0:
            return SureBetCheckResult(is_sure_bet=True, for_opponent_1_winning=True, for_opponent_2_winning=False)

        if (1 / bet_1.odds_2) + (1 / bet_2.odds_1) < 1.0:
            return SureBetCheckResult(is_sure_bet=True, for_opponent_1_winning=False, for_opponent_2_winning=True)

        return SureBetCheckResult(is_sure_bet=False, for_opponent_1_winning=False, for_opponent_2_winning=False)

    def _calculate_investment_for(
        self, odds_1: Decimal, odds_2: Decimal, total_stake: Decimal
    ) -> InvestmentCalculationResult:
        self._logger.info(f"Calculating surebet investment for {odds_1} and {odds_2}")

        x, y = symbols("x y")

        eq1 = Eq(x + y - total_stake, 0)  # total_stake = x + y
        eq2 = Eq((odds_2 * y) - odds_1 * x, 0)  # odds1*x = odds2*y

        stakes = solve((eq1, eq2), (x, y))

        total_investment = stakes[x] + stakes[y]

        profit1 = odds_1 * stakes[x] - total_stake
        profit2 = odds_2 * stakes[y] - total_stake

        benefit1 = f"{profit1 / total_investment * 100:.2f}%"
        benefit2 = f"{profit2 / total_investment * 100:.2f}%"

        return InvestmentCalculationResult(
            stake_1=Decimal(str(stakes[x])),
            stake_2=Decimal(str(stakes[y])),
            profit_1=Decimal(str(profit1)),
            profit_2=Decimal(str(profit2)),
            benefit_1=benefit1,
            benefit_2=benefit2,
        )

    def find(self) -> None:
        self._logger.info("Finding bets!")
        bets = self._repository.get_all_which_are_in_future()

        results = filter(lambda bets_pair: bets_pair[0] == bets_pair[1], itertools.combinations(bets, 2))

        for bet_1, bet_2 in results:
            surbet_check_result = self._is_surebet(bet_1, bet_2)

            if surbet_check_result.is_sure_bet and surbet_check_result.for_opponent_1_winning:
                calculation_result = self._calculate_investment_for(bet_1.odds_1, bet_2.odds_2, Decimal(100))
                sure_bet = SureBet(
                    id=ObjectId(),
                    bets=[bet_1.id, bet_2.id],
                    opponent_1=bet_1.opponent_1,
                    opponent_2=bet_2.opponent_2,
                    odds_for_opponent_1=bet_1.odds_1,
                    odds_for_opponent_2=bet_2.odds_2,
                    url_1=bet_1.get_full_url(),
                    url_2=bet_2.get_full_url(),
                    opponent_1_winning=True,
                    opponent_2_winning=False,
                    calculation_result=calculation_result,
                    created_at=datetime.utcnow(),
                )
                print(sure_bet.info())

            if surbet_check_result.is_sure_bet and surbet_check_result.for_opponent_2_winning:
                calculation_result = self._calculate_investment_for(bet_1.odds_2, bet_2.odds_1, Decimal(100))
                sure_bet = SureBet(
                    id=ObjectId(),
                    bets=[bet_1.id, bet_2.id],
                    opponent_1=bet_1.opponent_1,
                    opponent_2=bet_2.opponent_2,
                    odds_for_opponent_1=bet_1.odds_1,
                    odds_for_opponent_2=bet_2.odds_2,
                    url_1=bet_1.get_full_url(),
                    url_2=bet_2.get_full_url(),
                    opponent_1_winning=False,
                    opponent_2_winning=True,
                    calculation_result=calculation_result,
                    created_at=datetime.utcnow(),
                )
                print(sure_bet.info())
