from typing import List, Protocol

from surebets_finder.shared.category import Category
from surebets_finder.shared.reflection import raises


class UrlStrategy(Protocol):
    def get_urls(self) -> List[str]:
        ...


class EFortunaUrlStrategy(UrlStrategy):
    def __init__(self, category: Category) -> None:
        self._category = category

    @raises(ValueError)
    def get_urls(self) -> List[str]:
        if self._category == Category.ESPORT:
            return [
                "https://www.efortuna.pl/zaklady-bukmacherskie/esport-cs-go?selectDates=1",
                "https://www.efortuna.pl/zaklady-bukmacherskie/esport-lol?selectDates=1",
                "https://www.efortuna.pl/zaklady-bukmacherskie/esport-dota2?selectDates=1",
                "https://www.efortuna.pl/zaklady-bukmacherskie/esport-starcraft-2?selectDates=1",
                "https://www.efortuna.pl/zaklady-bukmacherskie/esport-rainbow-six?selectDates=1",
                "https://www.efortuna.pl/zaklady-bukmacherskie/esport-pozosta%C5%82e?selectDates=1",
            ]

        raise ValueError(
            f"Category `{self._category.value}` is not a correct value. Possible value {Category.values()}"
        )


class BetClickUrlStrategy(UrlStrategy):
    def __init__(self, category: Category) -> None:
        self._category = category

    @raises(ValueError)
    def get_urls(self) -> List[str]:
        if self._category == Category.ESPORT:
            return [
                "https://offer.cdn.begmedia.com/api/pub/v4/events?application=2048&countrycode=pl&fetchMultipleDefaultMarkets=true&language=pa&limit=1000&offset=0&sitecode=plpa&sortBy=ByLiveRankingPreliveDate&sportIds=102"
            ]

        raise ValueError(
            f"Category `{self._category.value}` is not a correct value. Possible value {Category.values()}"
        )


class LVBetUrlStrategy(UrlStrategy):
    def __init__(self, category: Category) -> None:
        self._category = category

    @raises(ValueError)
    def get_urls(self) -> List[str]:
        if self._category == Category.ESPORT:
            return [
                "https://app.lvbet.pl/_api/v1/offer/matches/?is_live=false&sports_groups_ids=41071,42981,43200,43415,44564,45586,45649,43555,43910,45644,45647,9870,9964,41592,44058,1168,45642,5878,2806,45595,45609,45619,45670&lang=pl"
            ]

        raise ValueError(
            f"Category `{self._category.value}` is not a correct value. Possible value {Category.values()}"
        )
