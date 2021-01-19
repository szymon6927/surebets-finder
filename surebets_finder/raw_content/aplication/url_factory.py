from surebets_finder.raw_content.aplication.url_strategy import (
    BetClickUrlStrategy,
    EFortunaUrlStrategy,
    LVBetUrlStrategy,
    UrlStrategy,
)
from surebets_finder.shared.category import Category
from surebets_finder.shared.provider import Provider
from surebets_finder.shared.reflection import raises


class UrlFactory:
    @classmethod
    @raises(ValueError)
    def create(cls, provider: Provider, category: Category) -> UrlStrategy:
        if provider == Provider.EFORTUNA:
            return EFortunaUrlStrategy(category)

        if provider == Provider.BETCLICK:
            return BetClickUrlStrategy(category)

        if provider == Provider.LVBET:
            return LVBetUrlStrategy(category)

        raise ValueError(f"Provider `{provider.value}` is not a suitable choice!")
