from surebets_finder.bet.application.bet_finder import EFortunaBetFinder
from surebets_finder.bet.application.bet_finder_factory import BetFinderFactory
from surebets_finder.shared.provider import Provider


def test_bet_finder_factory_should_return_correct_instance_when_provider_is_correct() -> None:
    # given
    bet_finder = BetFinderFactory.create(Provider.EFORTUNA)

    # then
    assert isinstance(bet_finder, EFortunaBetFinder)
