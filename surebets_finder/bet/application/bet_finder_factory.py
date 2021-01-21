from surebets_finder.bet.application.bet_finder import BetClickBetFinder, BetFinder, EFortunaBetFinder, LVBetBetFinder
from surebets_finder.shared.provider import Provider
from surebets_finder.shared.reflection import raises


class BetFinderFactory:
    @classmethod
    @raises(ValueError)
    def create(cls, provider: Provider) -> BetFinder:
        if provider == Provider.EFORTUNA:
            return EFortunaBetFinder()  # type: ignore

        if provider == Provider.BETCLICK:
            return BetClickBetFinder()  # type: ignore

        if provider.LVBET:
            return LVBetBetFinder()  # type: ignore

        raise ValueError(f"Provider `{provider.value}` is not a suitable choice!")
