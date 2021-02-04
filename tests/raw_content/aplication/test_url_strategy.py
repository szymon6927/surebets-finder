from surebets_finder.raw_content.aplication.url_strategy import (
    BetClickUrlStrategy,
    EFortunaUrlStrategy,
    LVBetUrlStrategy,
)
from surebets_finder.shared.category import Category


def test_efortuna_url_strategy_return_list_of_urls() -> None:
    # given
    strategy = EFortunaUrlStrategy(Category.ESPORT)

    # when
    result = strategy.get_urls()

    # then
    assert isinstance(result[0], str)


def test_betclick_url_strategy_return_list_of_urls() -> None:
    # given
    strategy = BetClickUrlStrategy(Category.ESPORT)

    # when
    result = strategy.get_urls()

    # then
    assert isinstance(result[0], str)


def test_lvbet_url_strategy_return_list_of_urls() -> None:
    # given
    strategy = LVBetUrlStrategy(Category.ESPORT)

    # when
    result = strategy.get_urls()

    # then
    assert isinstance(result[0], str)
