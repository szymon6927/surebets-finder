from typing import Any

import pytest

from surebets_finder.raw_content.aplication.url_factory import UrlFactory
from surebets_finder.raw_content.aplication.url_strategy import (
    BetClickUrlStrategy,
    EFortunaUrlStrategy,
    LVBetUrlStrategy,
)
from surebets_finder.shared.category import Category
from surebets_finder.shared.provider import Provider


@pytest.mark.parametrize(
    "provider, strategy_type",
    [
        (Provider.EFORTUNA, EFortunaUrlStrategy),
        (Provider.LVBET, LVBetUrlStrategy),
        (Provider.BETCLICK, BetClickUrlStrategy),
    ],
)
def test_url_factory_should_return_correct_instance_when_provider_is_correct(
    provider: Provider, strategy_type: Any
) -> None:
    # given
    strategy = UrlFactory.create(provider, Category.ESPORT)

    # then
    assert isinstance(strategy, strategy_type)
